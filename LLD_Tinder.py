from typing import Dict, List


class User:
    idx: str
    name: str
    pictures: List[str]
    location: int
    radius: int

    def __init__(self, idx, name, pictures, location, radius):
        self.idx = idx
        self.name = name
        self.pictures = pictures
        self.location = location
        self.radius = radius

    def get_id(self):
        return self.idx

    def change_radius(self, radius):
        self.radius = radius

    def get_location(self) -> int:
        return int(self.location)


class Chat:
    message: str
    sender: User

    def __init__(self, message, sender):
        self.message = message
        self.sender = sender


class Match:
    a: User
    b: User
    id: str
    chats: List[Chat]

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add_message(self, chat):
        self.chats.append(chat)


class Swipes:

    users: Dict[str, User]

    def has_swiped(self, user):
        if user in self.users:
            return True
        return False

    def add_to_swipe(self, user) -> None:
        self.users[user.get_id()] = user

    def is_swiped_by(self, user) -> bool:
        if self.users[user.get_id()]:
            return True
        return False


class System:
    users: List[User]
    matches: Dict[str, List[Match]]
    left_swipe: Dict[str, Swipes]
    right_swipe: Dict[str, Swipes]
    suggestions: Dict[str, List[User]]

    def recommend(self, user: User) -> List[User]:
        user_list = self.suggestions.get(user.get_id())
        self.suggestions = self.suggestions.get(user.get_id())[6:]  # removing first 5
        return user_list

    def swipe_left(self, a: User, b: User) -> None:
        self.left_swipe[a.get_id()].add_to_swipe(b)

    def swipe_right(self, a: User, b: User) -> None:
        self.right_swipe[a.get_id()].add_to_swipe(b)
        if self.right_swipe[b.get_id()].is_swiped_by(a):
            match = self.create_match(a=a, b=b)
            self.matches[a.get_id()].append(match)
            self.matches[b.get_id()].append(match)

    @staticmethod
    def create_match(a: User, b: User) -> Match:
        return Match(a=a, b=b)

    def change_radius(self, user: User, radius: int) -> None:
        new_suggestions: List[User] = []
        user.change_radius(radius)
        for i in range(len(self.users)):
            if self.left_swipe.get(user.get_id()).has_swiped(self.users[i]) or \
                 self.right_swipe.get(user.get_id()).has_swiped(self.users[i]):
                continue
            if (self.users[i].get_location() - user.get_location()) < radius:
                new_suggestions.append(self.users[i])

        self.suggestions[user.get_id()] = new_suggestions

    @staticmethod
    def send_message(chat: Chat, match: Match) -> None:
        match.add_message(chat=chat)

    def un_match(self, a: User, b: User, match: Match) -> None:
        self.matches[a.get_id()].remove(match)
        self.matches[b.get_id()].remove(match)
