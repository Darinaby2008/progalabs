from pathlib import Path
from tempfile import TemporaryDirectory
from .console_view import ConsoleView
from .core.dice import Dice
from .combat.outcome import Outcome
from .defense.damage import Damage
from .defense.armor_handler import ArmorHandler
from .defense.barrier_handler import BarrierHandler
from .defense.evasion_handler import EvasionHandler
from .enemy.goblin import Goblin
from .enemy.dragon import Dragon
from .enemy.legendary_enemy import LegendaryEnemy
from .enemy.windfury_enemy import WindfuryEnemy
from .enemy.armored_enemy import ArmoredEnemy
from .enemy.haunted_weapon import HauntedWeapon
from .hero.hero import Hero
from .hero.hero_class import HeroClass
from .item.default_catalog import create_default_catalog, ELVEN_BOW
from .tactic.balanced_tactic import BalancedTactic
from .tactic.aggressive_tactic import AggressiveTactic
from .tactic.cautious_tactic import CautiousTactic
from .world.crypt import Crypt
from .world.forest import Forest
from .world.haunted_manor import HauntedManor
from .event.game_event import GameEvent
from .event.game_event_type import GameEventType
from .event.game_event_publisher import GameEventPublisher
from .progress.achievement_tracker import AchievementTracker
from .progress.expedition_journal import ExpeditionJournal
from .storage.file_hero_repository import FileHeroRepository
from .storage.caching_hero_repository import CachingHeroRepository
from .game.game_facade import GameFacade

def main() -> None:
    catalog = create_default_catalog()
    view = ConsoleView()

    print("===== Адаптер =====")
    bow = catalog.create_weapon(ELVEN_BOW)
    haunted = HauntedWeapon(bow)
    print(f"Оружие {bow.name} стало врагом: {haunted.name} (здоровье {haunted.max_health})")

    print("\n===== Декоратор =====")
    goblin = Goblin()
    print(f"Обычный враг: {goblin.name}, урон {goblin.roll_damage().damage}")
    elite = ArmoredEnemy(WindfuryEnemy(LegendaryEnemy(goblin)))
    print(f"Элитный враг: {elite.name}, урон {elite.roll_damage().damage}")
    print(f"Элитный враг получает 100 урона, но пропускает только: {elite.receive_hit(100).amount}")

    print("\n===== Заместитель =====")
    with TemporaryDirectory() as tmp_dir:
        save_file = Path(tmp_dir) / "heroes.json"
        repo = FileHeroRepository(save_file, catalog)
        cached_repo = CachingHeroRepository(repo)
        
        hero_dummy = Hero.Builder().set_name("Тест").set_hero_class(HeroClass.WARRIOR).set_starter_kit(HeroClass.WARRIOR.starter_kit(catalog)).build()
        cached_repo.save(hero_dummy)
        print(f"Герой сохранен. Поиск из кэша: {cached_repo.find_by_name('Тест') is not None}")

    print("\n===== Стратегия =====")
    hero = Hero.Builder().set_name("Стратег").set_hero_class(HeroClass.WARRIOR).set_starter_kit(HeroClass.WARRIOR.starter_kit(catalog)).build()
    enemy = Goblin()
    print(f"Баланс: {BalancedTactic().choose_action(1, hero, enemy)}")
    print(f"Натиск: {AggressiveTactic().choose_action(1, hero, enemy)}")
    print(f"Осторожность: {CautiousTactic().choose_action(1, hero, enemy)}")

    print("\n===== Наблюдатель =====")
    publisher = GameEventPublisher()
    achievements = AchievementTracker()
    journal = ExpeditionJournal()
    publisher.subscribe(GameEventType.VICTORY, achievements)
    publisher.subscribe(GameEventType.VICTORY, journal)
    print("Подписчики (Ачивки и Журнал) подписаны на событие 'Победа'.")

    print("\n===== Цепочка обязанностей =====")
    armor = ArmorHandler(0.5) # 50% защиты
    barrier = BarrierHandler(10) # 10 единиц щита
    evasion = EvasionHandler(1.0) # 100% шанс уклонения (для демо)
    
    evasion.set_next(armor).set_next(barrier)
    
    d1 = Damage(50)
    evasion.handle(d1)
    print(f"Урон 50 через цепочку (уклонение): {d1.amount} урона, уклонение={d1.evaded}")
    
    evasion_no_dodge = ArmorHandler(0.5)
    evasion_no_dodge.set_next(BarrierHandler(10))
    d2 = Damage(50)
    evasion_no_dodge.handle(d2)
    print(f"Урон 50 через цепочку (броня+барьер): {d2.amount} урона, поглощено={d2.absorbed}")

    print("\n===== Фасад =====")
    with TemporaryDirectory() as tmp_dir:
        game = GameFacade(Path(tmp_dir) / "save.json")
        print(f"Фасад создал игру. Доступно локаций: {len(game.locations)}")
        print(f"Доступно тактик: {len(game.tactics)}")
        test_hero = game.create_hero("Фасадный", HeroClass.MAGE.code)
        print(f"Герой создан через фасад: {test_hero.name}")

if __name__ == "__main__":
    main()