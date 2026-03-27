# Блок 2

# 7.4. (уровень сложности: высокий)
# Переработайте игровой движок таким образом, чтобы поддерживалась генерация
# html-проекта для игры в Web. Поддержите также вывод графики в формате игрового мира.

# 7.5. (уровень сложности: высокий)
# Реализуйте инструмент для автоматической проверки игрового мира на наличие 
# тупиков – мест, из которых нельзя добраться до завершения игры.


import re
import os
from collections import deque
from typing import Dict, List, Set, Optional

class AdventureEngine:
    def __init__(self):
        self.rooms: Dict[str, dict] = {}
        self.start_room: Optional[str] = None
        self.win_labels: Set[str] = set()

    def parse(self, text: str) -> None:
        room_p = re.compile(r'\[ROOM\s+(\w+)\]\s*(.*)')
        act_p = re.compile(r'\[ACT\s+(\w+)\]\s*(.*)')
        
        current_room = None
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line: continue
            
            room_m = room_p.match(line)
            if room_m:
                label, title = room_m.groups()
                current_room = {
                    'label': label, 'title': title, 'desc': [],
                    'actions': [], 'image': None
                }
                self.rooms[label] = current_room
                if self.start_room is None: self.start_room = label
                if 'win' in label.lower(): self.win_labels.add(label)
                continue
            
            if not current_room: continue

            if line.startswith('[DESC]'):
                current_room['desc'].append(line.replace('[DESC]', '').strip())
            elif line.startswith('[IMAGE]'):
                current_room['image'] = line.replace('[IMAGE]', '').strip()
            else:
                act_m = act_p.match(line)
                if act_m:
                    target, act_text = act_m.groups()
                    current_room['actions'].append((act_text, target))
                    if target.lower() == 'win':
                        self.win_labels.add(current_room['label'])

    # 7.5
    def find_dead_ends(self) -> List[str]:
        if not self.start_room: return []

        reachable = {self.start_room}
        queue = deque([self.start_room])
        while queue:
            curr = queue.popleft()
            for _, target in self.rooms[curr]['actions']:
                if target in self.rooms and target not in reachable:
                    reachable.add(target)
                    queue.append(target)

        reverse_graph = {label: [] for label in self.rooms}
        for label, room in self.rooms.items():
            for _, target in room['actions']:
                if target in self.rooms:
                    reverse_graph[target].append(label)

        safe_rooms = set()
        back_queue = deque()
        
        for label in self.win_labels:
            if label in self.rooms:
                safe_rooms.add(label)
                back_queue.append(label)
        for label, room in self.rooms.items():
            if any(t.lower() == 'win' for _, t in room['actions']) and label not in safe_rooms:
                safe_rooms.add(label)
                back_queue.append(label)

        while back_queue:
            curr = back_queue.popleft()
            for prev in reverse_graph.get(curr, []):
                if prev not in safe_rooms:
                    safe_rooms.add(prev)
                    back_queue.append(prev)

        return [r for r in reachable if r not in safe_rooms]

    # 7.4 
    def export_html(self, output_dir: str = 'game_html') -> str:
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'css'), exist_ok=True)
        
        with open(os.path.join(output_dir, 'css', 'style.css'), 'w', encoding='utf-8') as f:
            f.write(self._get_css())
        
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(self._generate_main_html())
        
        for label, room in self.rooms.items():
            with open(os.path.join(output_dir, f'{label}.html'), 'w', encoding='utf-8') as f:
                f.write(self._generate_room_html(room))
        return f"HTML-проект: {os.path.abspath(output_dir)}"

    def _get_css(self) -> str:
        return """
        body { font-family: sans-serif; background: #1a1a1a; color: #ccc; display: flex; justify-content: center; padding: 20px; }
        .card { max-width: 600px; width: 100%; background: #252525; padding: 25px; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.5); }
        .room-img { width: 100%; border-radius: 5px; margin-bottom: 15px; border: 1px solid #444; }
        .btn { display: block; padding: 12px; margin: 10px 0; background: #4a90e2; color: white; text-decoration: none; border-radius: 5px; text-align: center; }
        .btn:hover { background: #357abd; }
        .status { padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; }
        .win { background: #2d5a27; } .dead { background: #5a2727; }
        """

    def _generate_main_html(self) -> str:
        return f"<html><head><link rel='stylesheet' href='css/style.css'></head><body><div class='card'><h1>Начало лабиринта</h1><p>Вы в начале лабиринта. Сможете ли из него выбраться?    </p><a href='{self.start_room}.html' class='btn'>Начать</a></div></body></html>"

    def _generate_room_html(self, room: dict) -> str:
        img = f"<img src='{room['image']}' class='room-img'>" if room['image'] else ""
        actions = ""
        if not room['actions']:
            status_class = "win" if room['label'] in self.win_labels else "dead"
            status_text = "ПОБЕДА!" if room['label'] in self.win_labels else "ТУПИК"
            actions = f"<div class='status {status_class}'>{status_text}</div>"
        else:
            for text, target in room['actions']:
                link = f"{target}.html" if target.lower() != 'win' else "index.html"
                actions += f"<a href='{link}' class='btn'>{text}</a>"
        
        return f"""<html><head><link rel='stylesheet' href='css/style.css'></head><body><div class='card'>
        <h2>{room['title']}</h2>{img}<p>{'<br>'.join(room['desc'])}</p>{actions}
        <br><a href='index.html' style='color:#666'>В начало</a></div></body></html>"""

    def play_terminal(self):
        curr = self.start_room
        while curr and curr in self.rooms:
            room = self.rooms[curr]
            print(f"\n[{room['title']}]")
            if room['image']: print(f"(Картинка: {room['image']})")
            print("\n".join(room['desc']))
            if not room['actions']:
                print("--- КОНЕЦ ---")
                break
            for i, (txt, _) in enumerate(room['actions'], 1): print(f"{i}. {txt}")
            try:
                idx = int(input("> ")) - 1
                target = room['actions'][idx][1]
                if target.lower() == 'win':
                    print("🏆 ПОБЕДА!"); break
                curr = target
            except: print("Ошибка ввода")

if __name__ == '__main__':
    game_text = """
[ROOM 1] Древние ворота
[DESC] Вы стоите у высоких, древних ворот, ведущих в лабиринт, чьи стены уходят в туман.
[DESC] Воздух здесь прохладный, и где-то вдалеке слышится эхо капающей воды.
[ACT 2] Проход на запад

[ROOM 2] Комната с рунами
[DESC] Вы находитесь в узкой, извилистой комнате.
[DESC] Стены украшены древними рунами, светящимися слабым светом.
[ACT 3] Проход на запад
[ACT 1] Проход на восток

[ROOM 3] Подземное озеро
[DESC] Эта комната напоминает подземное озеро. Вода мерцает зелёным светом.
[DESC] В центре комнаты стоит древний каменный алтарь.
[ACT 4] Проход на север
[ACT 2] Проход на восток

[ROOM 4] Зал колонн
[DESC] Вы оказались в огромной зале, поддерживаемой колоннами из чёрного камня.
[DESC] В центре горит вечный огонь, освещая древние фрески.
[ACT 5] Проход на север
[ACT 3] Проход на юг

[ROOM 5] Комната шёпота
[DESC] Эта комната наполнена странными звуками, похожими на шёпот ветра.
[DESC] На стенах висят старинные ковры, изображающие сцены из легенд.
[ACT 4] Проход на юг
[ACT 6] Проход на восток

[ROOM 6] Зеркальная комната
[DESC] Воздух наполнен запахом мёда и лаванды.
[DESC] На стенах развешаны зеркала, искажающие ваше отражение.
[ACT 15] Проход на север
[ACT 7] Проход на юг
[ACT 5] Проход на запад
[ACT 11] Проход на восток

[ROOM 7] Библиотечный зал
[DESC] Комната напоминает древнюю библиотеку. 
[DESC] Полки, уходящие вверх, полны старинных книг и свитков.
[ACT 6] Проход на север
[ACT 8] Проход на восток

[ROOM 8] Тронный зал
[DESC] Вы находитесь в тронном зале. 
[DESC] В центре стоит пустой трон, окружённый статуями древних стражей.
[ACT 7] Проход на запад
[ACT 9] Проход на восток

[ROOM 9] Подземный водопад
[DESC] Эта комната полна звуков падающей воды.
[DESC] Брызги водопада создают радугу в воздухе.
[ACT 10] Проход на юг
[ACT 8] Проход на запад

[ROOM 10] Влажная пещера (Тупик)
[DESC] Вы находитесь в пещере, где воздух насыщен влагой.
[DESC] На стенах видны следы древних наскальных рисунков. Дальше пути нет.
[ACT 9] Обратно к водопаду

[ROOM 11] Светящийся сад
[DESC] Сад, выращенный в подземелии. 
[DESC] Растения светятся мягким светом, создавая атмосферу спокойствия.
[ACT 6] Проход на запад
[ACT 12] Проход на восток

[ROOM 12] Комната мозаик
[DESC] Стены украшены мозаиками из древних легенд. 
[DESC] В центре стоит фонтан с кристально чистой водой.
[ACT 13] Проход на север
[ACT 11] Проход на запад

[ROOM 13] Древний храм
[DESC] Эта комната напоминает храм. В центре стоит монолит со странными символами.
[DESC] Воздух здесь наэлектризован.
[ACT 12] Проход на юг
[ACT 14] Проход на запад

[ROOM 14] Замшелая комната (Тупик)
[DESC] Стены покрыты мхом, а воздух наполнен запахом земли. 
[DESC] Древнее дерево уходит корнями глубоко вниз.
[ACT 13] Проход обратно к храму

[ROOM 15] Зал портала
[DESC] Свет исходит из кристаллов на стенах. 
[DESC] В центре стоит портал, светящийся ярким белым светом.
[ACT win] Проход на север (Выход из лабиринта)
[ACT 6] Проход на юг
[ACT 16] Проход на запад

[ROOM 16] Хранитель карты
[DESC] Кристаллы издают мелодичные звуки. 
[DESC] На каменной плите высечена полная карта лабиринта.
[ACT 15] Проход на восток
"""

    engine = AdventureEngine()
    engine.parse(game_text)
    
    dead_ends = engine.find_dead_ends()
    if dead_ends:
        print(f"⚠️ Найдены тупики: {', '.join(dead_ends)}")
    else:
        print("✅ Тупиков не обнаружено.")

    print(engine.export_html('adventure_web'))
    
    # engine.play_terminal()