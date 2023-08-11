from python_graphql_client import GraphqlClient

# create a client instance
client = GraphqlClient(endpoint="https://api.catgirl.io/graphql")

# define the query as a string
query = """
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
}
"""

while True:
  # define the variables
  variables = {
      "id": input("Enter the ID: ")  # Replace with the actual ID value you want to query for
  }

  # make the query and get the response
  result = client.execute(query=query, variables=variables)

  # print the response
  print(result)
