from python_graphql_client import GraphqlClient
from discord.ext import commands
import json
import datetime
import discord
import os

class nftLookup:
    def __init__(self, discord_client, client = "https://api.catgirl.io/graphql"):
        self.allowed_channel = 954121009538170881
        # create a client instance
        self.client = GraphqlClient(endpoint=client)
        # define the query as a string
        self.query = """
        query ($id: ID!) {
        catgirlNFT(id: $id) {
            tokenId
            ownerAddress
            characterId
            season
            rarity
            nyaScore
            bornAt
            isSleeping
            }
        }"""
        self.catgirls = { (1, 0, 0): "Mae", (1, 1, 0): "Kita", (1, 2, 0): "Hana", (1, 3, 0): "Celeste", (1, 4, 0): "Mittsy", (1, 0, 1): "Lisa", (1, 1, 1): "Aoi", (1, 2, 1): "Rin",
        (2, 0, 0): "Mae", (2, 0, 1): "Ruby", (2, 0, 2): "Eve", (2, 1, 0): "Coco", (2, 1, 1): "Lulu", (2, 2, 0): "Yuna", (2, 2, 1): "Grace", (2, 3, 0): "Raven", (2, 3, 1): "Maiko", (2, 4, 0): "FeLinE:1000x" }
        self.thumbnail_dict = {'aoi': 'gOnXyEQ', 'celeste': '0UW8571', 'coco': 'IIOduqA', 'eve': 'j0I7AcL', 'feline:1000x': 'GCyHla8', 'grace': 'nrDLosU', 'hana': 'V5AiDUh',
        'kita': 'yvUI9Up', 'lisa': 'aLOi6En', 'lulu': 'YRDdaeP', 'mae1': 'c3Vi8cl', 'mae2': '4Gek6jz', 'maiko': 'bp8xboQ', 'mittsy': 'mSp84cG', 'raven': 's8wYBZn',
        'rin': 'LuWEefb', 'ruby': '87aEcd9', 'yuna': 'EQhpUgP'}
        self.discord_client = discord_client
    
    def __search_nft_by_id(self, id: str):
        # define the variables
        variables = {
            "id": id  # Replace with the actual ID value you want to query for
        }
        # make the query and get the response
        result = dict(self.client.execute(query = self.query, variables=variables)).get("data")
        return result.get("catgirlNFT")
    
    def __get_catgirl_name(self, season: int, character_id: int, rarity: int) -> str:
        try:
            return self.catgirls[(season, character_id, rarity)]
        except KeyError:
            return "Unknown Catgirl!"

    def __parseTimesamp(self, timestamp: int) -> str:
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        date_string = dt_object.strftime("%Y.%m.%d")
        time_string = dt_object.strftime("%H:%M:%S")
        return " ".join([date_string, time_string])

    def __parse_nft_info(self, id):
        star_emoji = lambda rarity: '⭐' * (rarity+1) if rarity in range(5) else ''
        nft = self._nftLookup__search_nft_by_id(str(id))
        parsed_info = {"id": None, "owner": "0x000000000000000000000000000000000000dead", "charId": 0, "season": None, "rarity": 0, "nya": 0, "dob": 0, "sleeping": None, "name": "Unknown NFT", "tofuUrl": None, "stars": None}
        try:
            parsed_info["id"] = nft.get("tokenId")
            parsed_info["owner"] = nft.get("ownerAddress")
            parsed_info["charId"] = nft.get("characterId")
            parsed_info["season"] = nft.get("season")
            parsed_info["rarity"] = nft.get("rarity")
            parsed_info["nya"] = nft.get("nyaScore")
            parsed_info["dob"] = self._nftLookup__parseTimesamp(nft.get("bornAt"))
            parsed_info["sleeping"] = nft.get("isSleeping")
            parsed_info["name"] = self._nftLookup__get_catgirl_name(parsed_info["season"], parsed_info["rarity"], parsed_info["charId"])
            #parsed_info["tofuUrl"] = f"https://tofunft.com/nft/bsc/0xE796f4b5253a4b3Edb4Bb3f054c03F147122BACD/{parsed_info['id']}"
            parsed_info["Url"] = f"https://app.catgirl.io/marketplace/details/{parsed_info['id']}"
            parsed_info["stars"] = star_emoji(parsed_info["rarity"])
        except AttributeError:
            pass
        return parsed_info

    def __makeNFTEmbed(self, id):
        nft_dict = self._nftLookup__parse_nft_info(str(id))
        rarity = nft_dict['rarity']
        embed = discord.Embed(title=f"Results for NFT with id {nft_dict['id']}:", description=f"Mae's NFT Lookup")

        # Check if an image with the name of the NFT exists in the nft folder
        nft_name = (lambda x: 'mae1' if x['name'].lower() == 'mae' and x['season'] == 1 else 'mae2' if x['name'].lower() == 'mae' and x['season'] == 2 else x['name'].lower())(nft_dict)
        thumbnail_url = self.thumbnail_dict.get(nft_name, 'xN0yNXw')
        # Set the thumbnail to the image file
        embed.set_thumbnail(url=f"https://i.imgur.com/{thumbnail_url}.png")

        embed.add_field(name='Name', value=nft_dict['name'], inline=False)
        embed.add_field(name='Rarity', value=nft_dict['stars'], inline=True)
        embed.add_field(name='Nya Score', value=nft_dict['nya'], inline=True)
        embed.add_field(name='Season', value=nft_dict['season'], inline=True)
        embed.add_field(name='Birthdate', value=nft_dict['dob'], inline=False)
        embed.add_field(name='Owner', value=f"[{nft_dict['owner'][:8]}...{nft_dict['owner'][-8:]}](https://bscscan.com/address/{nft_dict['owner']})", inline=False)
        embed.add_field(name='Sleeping', value=nft_dict['sleeping'], inline=True)
        embed.add_field(name='Marketplace Link', value=f"[Marketplace Link]({nft_dict['Url']})", inline=True)

        # Set embed colour based on rarity
        if rarity == 0:
            embed.color = discord.Color.from_rgb(121, 132, 173)
        elif rarity == 1:
            embed.color = discord.Color.from_rgb(20, 203, 158)
        elif rarity == 2:
            embed.color = discord.Color.from_rgb(254, 173, 98)
        elif rarity == 3:
            embed.color = discord.Color.from_rgb(114, 56, 240)
        elif rarity == 4:
            embed.color = discord.Color.from_rgb(213, 74, 142)

        return embed

    async def check_message(self, interaction, id: int):
        channel = interaction.channel
        if channel.id != self.allowed_channel:
            return None
        embed = self._nftLookup__makeNFTEmbed(id)
        return embed    
'''
    async def check_message(self, message):
        parse_nft_query = lambda s: int(s.split()[1]) if len(s.split()) == 2 and s.split()[0] == "!nft" and s.split()[1].isdigit() else "Incorrect format, please make your query as \"!nft #\" where # is the ID of the NFT you want to search."
        channel = self.discord_client.get_channel(message.channel.id)
        if channel.id != self.allowed_channel:
            return False
        id = parse_nft_query(message.content)
        if not isinstance(id, int):
            await channel.send(id)
            return False
        embed = self._nftLookup__makeNFTEmbed(id)
        await channel.send(embed = embed)
        return True
'''