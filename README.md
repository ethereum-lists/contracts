# Contracts List

This list is an effort to identify deployed contracts instances given their chain and address, by listing the project they belong to, along with some basic features. The goal is to be able to provide information about an address when a user is interacting with it, as well as tracking security contact information for known projects in the event that a vulnerability is found in a given contract address.

Example from `contracts/1/0x1F98431c8aD98523631AE4a59f267346ea31F984.json`:

```json
{
  "name": "UniswapV3 Factory",
  "contractName": "UniswapV3Factory",
  "project": "uniswap",
  "tags": ["factory"]
}
```

## Contracts entries

Each contract entry is stored in a separate file at `contracts/CHAINID/ADDRESS.json`, where the `CHAINID` is the EIP155 numeric identifier of the chain (as listed in chainlist.org), and `ADDRESS` is the checksummed deployment address. Each entry contains at least a `project` field, that maps to an entry in the `projects` folder (see below), as well as:

- `name`: User-friendly name of the contract
- `contractName`: Name of the contract in the Solidity source code
- `tags`: Properties of the contract, such as `factory` or `proxy`

Contract entries are validated against the [`contract.json`](./schemas/contract.json) JSON schema. Refer to it for the full specification of fields admitted in a contract entry.

## Projects entries

Each contract entry must map to an entry in `projects/PROJECT.json`, where `PROJECT` is a short name identifying a known project in the Ethereum space. Each project entry contains at least a user-friendly `name` field, and may contain links to the project website, social, token, entries in Coingecko or Everest, and emails for general contact and security disclosures:

- `website`: Main website of the project
- `contacts.contact`: General contact email
- `contacts.security`: Security contact email
- `token.chainId`: EIP155 identifier of the chain where the project token is deployed
- `token.address`: Address where the project token is deployed
- `token.name`: Name of the token
- `token.symbol`: Symbol of the token
- `token.decimals`: Decimals of the token contract
- `social.coingecko`: Path to the coingecko identifier
- `social.github`: Github organization slug
- `social.twitter`: Twitter account name
- `social.everest`: Identifier in the everest.link registry

Example from `projects/uniswap.json`:

```json
{
  "name": "Uniswap",
  "website": "https://uniswap.org/",
  "social": {
    "github": "Uniswap",
    "twitter": "Uniswap",
    "everest": "0xa2e07f422b5d7cbbfca764e53b251484ecf945fa",
    "coingecko": "coins/uniswap"
  },
  "token": {
    "chainId": 1,
    "address": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "symbol": "UNI",
    "name": "Uniswap",
    "decimals": 18
  },
  "contacts": {
    "contact": "contact@uniswap.org",
    "security": "security@uniswap.org"
  }
}
```

Project entries are validated against the [`project.json`](./schemas/project.json) JSON schema. Refer to it for the full specification of fields admitted in a project entry.

## Contributing

To add a new set of contracts and/or projects, open a pull request with the corresponding files. Make sure that they match the format required by the schemas, and that every contract entry has a corresponding project entry. Thanks for helping!

## Maintainers

- [OpenZeppelin](http://github.com/OpenZeppelin/)