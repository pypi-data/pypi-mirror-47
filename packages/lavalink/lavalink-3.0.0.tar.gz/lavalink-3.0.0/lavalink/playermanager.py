from .node import Node
from .models import BasePlayer
from .exceptions import NodeException


class PlayerManager:
    def __init__(self, lavalink, player):
        if not issubclass(player, BasePlayer):
            raise ValueError('Player must implement BasePlayer or DefaultPlayer.')

        self._lavalink = lavalink
        self.players = {}
        self.default_player = player

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        """ Returns an iterator that yields a tuple of (guild_id, player). """
        for guild_id, player in self.players.items():
            yield guild_id, player

    async def destroy(self, guild_id: int):
        """
        Removes a player from cache, and also Lavalink if applicable.
        Ensure you have disconnected the given guild_id from the voicechannel
        first, if connected.

        ONLY USE THIS IF YOU KNOW WHAT YOU'RE DOING!
        Usage of this function may lead to invalid cache states!

        ----------
        :param guild_id:
            The guild_id associated with the player to remove.
        """
        if guild_id not in self.players:
            return

        player = self.players.pop(guild_id)

        if player.node and player.node.available:
            await player.node._send(op='destroy', guildId=player.guild_id)

    def values(self):
        """ Returns an iterator that yields only values. """
        for player in self.players.values():
            yield player

    def find_all(self, predicate):
        """ Returns a list of players that match the given predicate. """
        if not predicate:
            return list(self.players.values())

        return [p for p in self.players.values() if bool(predicate(p))]

    def remove(self, guild_id: int):
        """ Removes a player from the internal cache. """
        if guild_id in self.players:
            player = self.players.pop(guild_id)
            player.cleanup()

    def get(self, guild_id: int):
        """
        Gets a player from cache.
        ----------
        :param guild_id:
            The guild_id associated with the player to get.
        """
        return self.players.get(guild_id)

    def create(self, guild_id: int, region: str = 'eu', endpoint: str = None, node: Node = None):
        """
        Creates a player if one doesn't exist with the given information.

        If node is provided, a player will be created on that node.
        If region is provided, a player will be created on a node in the given region.
        If endpoint is provided, Lavalink.py will attempt to parse the region from the endpoint
        and return a node in the parsed region.

        If node, region and endpoint are left unspecified, or region/endpoint selection fails,
        Lavalink.py will fall back to the node with the lowest penalty.

        Region can be omitted if node is specified and vice-versa.
        ----------
        :param guild_id:
            The guild_id to associate with the player.
        :param region:
            The region to use when selecting a Lavalink node.
        :param endpoint:
            The address of the Discord voice server.
        :param node:
            The node to put the player on.
        """
        if guild_id in self.players:
            return self.players[guild_id]

        if node:
            return node

        if endpoint:
            region = self._lavalink.node_manager.get_region(endpoint)

        node = self._lavalink.node_manager.find_ideal_node(region)

        if not node:
            raise NodeException('No available nodes!')

        self.players[guild_id] = player = self.default_player(guild_id, node)
        return player
