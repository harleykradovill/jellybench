import random

import httpx

from .base import BenchmarkScenario

SORT_ORDERS = [
    "SortName",
    "DateCreated",
    "PremiereDate",
    "ProductionYear",
    "CommunityRating",
    "Runtime",
    "Random",
    "Name",
]

FILTERS = [
    "IsFolder",
    "IsNotFolder",
    "IsUnplayed",
    "IsPlayed",
    "IsFavorite",
    "IsResumable",
]

ITEM_TYPES = [
    "Movie",
    "Series",
    "Season",
    "Episode",
    "MusicAlbum",
    "MusicArtist",
    "Audio",
    "Video",
    "BoxSet",
]

PAGE_SIZE = 50


class LibraryBenchmarkScenario(BenchmarkScenario):
    name = "Library"

    def __init__(self) -> None:
        self._user_id: str | None = None
        self._folder_ids: list[str] = []
        self._total_items = 0

    async def setup(self, client: httpx.AsyncClient) -> None:
        users = await client.get("/Users")
        users.raise_for_status()
        user_list = users.json()
        if user_list:
            self._user_id = user_list[0]["Id"]

        folders = await client.get("/Library/MediaFolders")
        folders.raise_for_status()
        self._folder_ids = [item["Id"] for item in folders.json().get("Items", [])]

        counts = await client.get("/Items/Counts", params={"userId": self._user_id})
        counts.raise_for_status()
        self._total_items = counts.json().get("Total", 0)

    async def run(self, client: httpx.AsyncClient) -> bool:
        action = random.choice(
            [
                self._browse_root,
                self._browse_folder,
                self._paginate,
                self._sort,
                self._filter,
                self._by_type,
                self._latest,
                self._counts,
            ]
        )
        return await action(client)

    async def _browse_root(self, client: httpx.AsyncClient) -> bool:
        resp = await client.get(
            "/Items",
            params={
                "userId": self._user_id,
                "recursive": True,
                "limit": PAGE_SIZE,
                "enableImages": False,
            },
        )
        return resp.status_code < 400

    async def _browse_folder(self, client: httpx.AsyncClient) -> bool:
        if not self._folder_ids:
            return True  # Nothing cached to browse
        resp = await client.get(
            "/Items",
            params={
                "userId": self._user_id,
                "parentId": random.choice(self._folder_ids),
                "recursive": True,
                "limit": PAGE_SIZE,
                "enableImages": False,
            },
        )
        return resp.status_code < 400

    async def _paginate(self, client: httpx.AsyncClient) -> bool:
        offset = random.randint(0, max(self._total_items - 1, 0))
        resp = await client.get(
            "/Items",
            params={
                "userId": self._user_id,
                "recursive": True,
                "startIndex": offset,
                "limit": PAGE_SIZE,
                "enableImages": False,
            },
        )
        return resp.status_code < 400

    async def _sort(self, client: httpx.AsyncClient) -> bool:
        resp = await client.get(
            "/Items",
            params={
                "userId": self._user_id,
                "recursive": True,
                "sortBy": random.choice(SORT_ORDERS),
                "sortOrder": random.choice(["Ascending", "Descending"]),
                "limit": PAGE_SIZE,
                "enableImages": False,
            },
        )
        return resp.status_code < 400

    async def _filter(self, client: httpx.AsyncClient) -> bool:
        resp = await client.get(
            "/Items",
            params={
                "userId": self._user_id,
                "recursive": True,
                "filters": random.choice(FILTERS),
                "limit": PAGE_SIZE,
                "enableImages": False,
            },
        )
        return resp.status_code < 400

    async def _by_type(self, client: httpx.AsyncClient) -> bool:
        resp = await client.get(
            "/Items",
            params={
                "userId": self._user_id,
                "recursive": True,
                "includeItemTypes": random.choice(ITEM_TYPES),
                "limit": PAGE_SIZE,
                "enableImages": False,
            },
        )
        return resp.status_code < 400

    async def _latest(self, client: httpx.AsyncClient) -> bool:
        resp = await client.get(
            "/Items/Latest",
            params={"userId": self._user_id, "limit": 20},
        )
        return resp.status_code < 400

    async def _counts(self, client: httpx.AsyncClient) -> bool:
        resp = await client.get("/Items/Counts", params={"userId": self._user_id})
        return resp.status_code < 400
