# Contracts List

This list is an effort to identify deployed contracts instances given their chain and address, by listing the project they belong to. The goal is to be able to provide information about an address when a user is interacting with it, as well as tracking security contact information for known projects in the event that a vulnerability is found in a given contract address.

**Work in progress.** The schema of the data may still change.

## Contributing

You can ensure to be notified of security vulnerabilities on your projects by adding your contracts and contact info here. Make sure to keep your project's info up to date.

### Existing projects and contracts

To add an existing project to this list, complete the form [here](https://github.com/ethereum-lists/contracts/issues/new?assignees=&labels=update+info&template=submit_info.yml&title=Update+info+for+PROJECT_NAME) including your project's name and security contact info, and a list of contracts deployed that belong to your project. This will automatically create a pull request that will be reviewed by one of the maintainers and merged. You can submit this form multiple times to update your info or register new deployments.

To simplify the process, please open the issue as a user of your project's Github organization. This will make it easier for maintainers to verify that you act on behalf of your project.

If you want to include additional information on your project, such as social links or an associated token, please send a pull request to add that info to the JSON files directly. See below for the data format, and make sure that any changes match the schemas, and that every contract entry has a corresponding project entry.

### Tracking new deployments

To automatically register security contact information for your project upon deployment, add a custom natspec tag `@custom:security-contact` with your contact email, and verify your contract's metadata on [Sourcify](http://sourcify.dev/). As an example:

```solidity
/**
 * @title An awesome contract
 * @custom:security-contact security@awesome.com
 */
contract Awesome { /* ... */ }
```

**Note**: Automatic import of natspec tags from Sourcify is not implemented, but we will crawl all previously verified contracts when ready. We recommend you start adding this tag to your contracts from now on so the security contact info gets added to the registry in the near future.

## Data format

All data is stored in JSON files, with one file per contract and per project. These files are validated against the JSON schemas in the `schemas` folder.

### Contracts entries

Each contract entry is stored in a separate file at `contracts/CHAINID/ADDRESS.json`, where the `CHAINID` is the EIP155 numeric identifier of the chain (as listed in chainlist.org), and `ADDRESS` is the EIP55 checksummed deployment address. Each entry contains at least a `project` field, that maps to an entry in the `projects` folder (see below), as well as:

- `name`: User-friendly name of the contract
- `contractName`: Name of the contract in the Solidity source code
- `source`: Where the contract entry was imported from
- `tags`: List of properties of the contract, such as `factory` or `proxy`
- `features`: Extended features of the contract

Example from `contracts/1/0x1F98431c8aD98523631AE4a59f267346ea31F984.json`:

```json
{
  "name": "UniswapV3 Factory",
  "contractName": "UniswapV3Factory",
  "project": "uniswap",
  "tags": ["factory"]
}
```

Contract entries are validated against the [`contract.json`](./schemas/contract.json) JSON schema. Refer to it for the full specification of fields admitted in a contract entry.

### Projects entries

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

## Acknowledgements

- [Dune Analytics](https://dune.xyz/) for providing an initial set of over 200,000 labelled contracts from their databases.

## Maintainers

- [OpenZeppelin](http://github.com/OpenZeppelin/)
- [Dune](https://github.com/duneanalytics)
