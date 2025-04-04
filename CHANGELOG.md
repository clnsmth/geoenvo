
# CHANGELOG



## v0.3.0 (2025-03-19)


### Build system

* build: downgrade python to improve accessibility ([`658f403`](https://github.com/clnsmth/geoenvo/commit/658f4031b284581834611008202a7b4487dfe85f)) 

### Documentation

* docs: WorldTerrestrialEcosystems defaults to centroid for polygons ([`3864f42`](https://github.com/clnsmth/geoenvo/commit/3864f426e1b5fd4c43a6cb86421a126ece05f155)) 
* docs: update UML diagram to current implementation ([`53aec6b`](https://github.com/clnsmth/geoenvo/commit/53aec6b1ad76821fc628d1b697ec9fcbc0ee26bb)) 
* docs: hide low level methods from api manual ([`6e18ed0`](https://github.com/clnsmth/geoenvo/commit/6e18ed01c48c7c2918669da51a017fce345d3e7a)) 
* docs: fix module import error ([`01ed721`](https://github.com/clnsmth/geoenvo/commit/01ed721fe3b5873ae834d05e066d5d2a19d20f08)) 
* docs: edit code comments for understanding ([`f7856df`](https://github.com/clnsmth/geoenvo/commit/f7856df211becd105c9822c387e8cac5f04c1d63)) 
* docs: enhance vocabulary mapping documentation ([`3a38cb5`](https://github.com/clnsmth/geoenvo/commit/3a38cb5ab4fb3d8afd2ef9cdfbf0d613414d47fd)) 
* docs: define scope of project ([`35c5565`](https://github.com/clnsmth/geoenvo/commit/35c5565795cbcb78a56bb94a955a6815974aafe9)) 
* docs: use alias import in docs for consistency ([`8a1bbe7`](https://github.com/clnsmth/geoenvo/commit/8a1bbe75f4f431581156e1235193a684495d6097)) 
* docs: deduplicate module level information for reduced clutter ([`da817ed`](https://github.com/clnsmth/geoenvo/commit/da817edc8668e39b4369d929fcf074b2ddf0f72f)) 
* docs: note EMU returns all vertically stacked environments if no z value is specified ([`6d0bc02`](https://github.com/clnsmth/geoenvo/commit/6d0bc02c437682d76ff624224954464aae384f95)) 
* docs: add data source DOIs to class modules for reference and understanding ([`214e2ab`](https://github.com/clnsmth/geoenvo/commit/214e2abad75ef6905a6f5a019be29c064269fefc)) 
* docs: clarify geometry handling variations across data sources ([`8c9b096`](https://github.com/clnsmth/geoenvo/commit/8c9b096668d8907120d1bc72988401baa83a37f3)) 
* docs: list supported geometry input format and types ([`d75a026`](https://github.com/clnsmth/geoenvo/commit/d75a02692ee16b8f42aeb3650f2b77eb4836f3e4)) 
* docs: add docstrings to utilities and environment modules for understanding ([`7c6c098`](https://github.com/clnsmth/geoenvo/commit/7c6c09834fdd6f2bf71811a49565c97b824fd0fc)) 
* docs: add docstrings to data source modules for understanding ([`e7c28d2`](https://github.com/clnsmth/geoenvo/commit/e7c28d2a207478413c0a390ce6a70d04a09af031)) 
* docs: add docstrings to geometry for user understanding ([`68df0a4`](https://github.com/clnsmth/geoenvo/commit/68df0a475b927afda01c23ba986311142b5b5a8c)) 
* docs: add docstrings to response module for user understanding ([`49e5ad8`](https://github.com/clnsmth/geoenvo/commit/49e5ad8cff3d6b5262b35590ee3017fee7c8534e)) 
* docs: create docstrings for the resolver module ([`df312c2`](https://github.com/clnsmth/geoenvo/commit/df312c22a25dfec5127e4b00d4fe7e980d3ba2fb)) 

### Features

* feat: implement logging and improve error handling ([`79e0510`](https://github.com/clnsmth/geoenvo/commit/79e05106904fac63411bdafbea6e71b30fd054fb)) 

### Refactoring

* refactor: reduce verbosity of logging info messages ([`048b12c`](https://github.com/clnsmth/geoenvo/commit/048b12ce14033ba7b310791bbae5587596b97e98)) 
* refactor: rename compile_response for clarity and specificity ([`7a1702a`](https://github.com/clnsmth/geoenvo/commit/7a1702a0bc347c9daf38f5d679a02410f11e66a7)) 
* refactor: address pylint issues (cont.) ([`c325076`](https://github.com/clnsmth/geoenvo/commit/c32507667a691e3ff5b5e9c4c955cd81cfc00989)) 
* refactor: address pylint issues ([`3715e5a`](https://github.com/clnsmth/geoenvo/commit/3715e5ad717c4f5e06f0b0db8e1c30369b8fa37f)) 
* refactor: migrate to ESRI server after USGS loss ([`ce60a45`](https://github.com/clnsmth/geoenvo/commit/ce60a453921582a570cbe831fbf9c2d9e9e06262)) 
* refactor: migrate to ESRI service after USGS loss ([`5d5043c`](https://github.com/clnsmth/geoenvo/commit/5d5043cd15bb709d2edeb0eaab08a9d8f89833c4)) 
* refactor: address confusion of two different resolve methods ([`e523fd0`](https://github.com/clnsmth/geoenvo/commit/e523fd028342ee8dda4c3e71baf76102d33c850d)) 
* refactor: create response module for organizing related functionality ([`168ccdb`](https://github.com/clnsmth/geoenvo/commit/168ccdbee1c3019a8639b7cd4457f002281c74e2)) 

### Testing

* test: update mock response objects ([`5dc20b6`](https://github.com/clnsmth/geoenvo/commit/5dc20b6b089806be2932a9f4652d2a68b2a5c072)) 

### Unknown

* tests: align name of test_get_attributes with method name ([`70b7815`](https://github.com/clnsmth/geoenvo/commit/70b7815842cb16f826a15ce0b2a1873b7d51fb5b))

* tests: address non-deterministic test_mock_response_content ([`71fecf6`](https://github.com/clnsmth/geoenvo/commit/71fecf62f2b426e324994373535a684d59feee57))

* tests: align test name with method name ([`9794a9a`](https://github.com/clnsmth/geoenvo/commit/9794a9a9ee059840afefc6c2b6c14a572c315ec1))

* tests: fix untested scenarios, and default to mocking ([`54eb116`](https://github.com/clnsmth/geoenvo/commit/54eb11659ed588bc88ce60cfc129f16d5a9f646f))


## v0.2.1 (2025-02-28)


### Bug fixes

* fix: improve semantics of "vocabulary" and "environmental property" ([`d43f13e`](https://github.com/clnsmth/geoenvo/commit/d43f13eb54e4e9527417a1b1afdabe0ab2649583)) 

### Documentation

* docs: document the data model of returned results ([`8e2cb39`](https://github.com/clnsmth/geoenvo/commit/8e2cb3941ba56d2c4c8803f84c4fca5d2fefd785)) 
* docs: trim the Schema.org from the basic example for brevity ([`cd3f612`](https://github.com/clnsmth/geoenvo/commit/cd3f6127900dc6f3d0642ed76b96d97497c455e6)) 
* docs: create design documentation ([`001cca7`](https://github.com/clnsmth/geoenvo/commit/001cca7d8e2b6b604ce6b7b043c24e64c4d30f2d)) 
* docs: declare modules for autodoc to build ([`27fd047`](https://github.com/clnsmth/geoenvo/commit/27fd04776550c8c8daa19e140323900a51510e81)) 
* docs: add class diagram to understand architecture ([`0413bd5`](https://github.com/clnsmth/geoenvo/commit/0413bd5a5b3d1d3f9cb1a969042ba75b7c32b6c4)) 
* docs: update class UML diagram for system understanding ([`7ad6d84`](https://github.com/clnsmth/geoenvo/commit/7ad6d843129d142831d65999dff3197808d1923f)) 
* docs: deprecate "vocabulary annotation" for "vocabulary mapping" ([`5bb2f7c`](https://github.com/clnsmth/geoenvo/commit/5bb2f7c480d706c34db602708953bc838abc5f3a)) 
* docs: deprecate `identify` and `query` for “resolve” ([`29c61fb`](https://github.com/clnsmth/geoenvo/commit/29c61fb0829a7e0f9945ac630002242d62492c55)) 
* docs: deprecate “Resolver” for “DataSource” (cont.) ([`ec222f4`](https://github.com/clnsmth/geoenvo/commit/ec222f4386332b3dcec2b4090d4a96d09e557b35)) 
* docs: deprecate “Resolver” for “DataSource” ([`9800aaf`](https://github.com/clnsmth/geoenvo/commit/9800aaf1d6d3b0042e4e941ca0e9ec3c82f7bcb5)) 

### Refactoring

* refactor: format for consistency ([`3ccdece`](https://github.com/clnsmth/geoenvo/commit/3ccdece1562897bb6b9313ffe352ae6b11b0280f)) 
* refactor: change name of Data class to Response to be more descriptive ([`329b45c`](https://github.com/clnsmth/geoenvo/commit/329b45c1704fe6893a03d0cc91b5484ace4f7883)) 
* refactor: format for consistency ([`302aa03`](https://github.com/clnsmth/geoenvo/commit/302aa035efd4a8301e8d47d8d1ceac267b5e2eb4)) 
* refactor: replace '._' with '.' for properties (cont.) ([`d576064`](https://github.com/clnsmth/geoenvo/commit/d576064640c8ba813dc2278d292d1410a3828918)) 
* refactor: change env_properties to properties ([`f183fe3`](https://github.com/clnsmth/geoenvo/commit/f183fe37a14b6d74282b522f59de433dee2d0421)) 
* refactor: format for consistency ([`5894180`](https://github.com/clnsmth/geoenvo/commit/589418044b1296d4da6b476b2c50f08319fbb539)) 
* refactor: deprecate "attributes" for "properties" (cont.) ([`0594043`](https://github.com/clnsmth/geoenvo/commit/05940431ad63115a6b5468409b84e48471b263d5)) 
* refactor: use "property" and "attribute" consistently ([`ef64638`](https://github.com/clnsmth/geoenvo/commit/ef64638f0b3968300acc027e0eeebb76310f5685)) 
* refactor:  import resolver classes to resolver module for intuitive client set up ([`8eab450`](https://github.com/clnsmth/geoenvo/commit/8eab45061e10329b58a670beca8111ee15d175fd)) 

### Testing

* test: rename tests/resolvers to tests/data_sources to align with source code ([`86a1892`](https://github.com/clnsmth/geoenvo/commit/86a1892c9cf966fd8e5b448edfbadec005ef3d36)) 
* test: update test fixture to fix outdated call ([`999045d`](https://github.com/clnsmth/geoenvo/commit/999045d18607c96073df45303affbb3027416f44)) 

## v0.2.0 (2025-02-14)


### Documentation

* docs: deprecate “ecosystem” for “environment” ([`994f1b3`](https://github.com/clnsmth/geoenvo/commit/994f1b305e2645684183eac5a1116167c0e75fb0)) 
* docs: resolve build warnings ([`417a252`](https://github.com/clnsmth/geoenvo/commit/417a252f6ff1beb003a57163cc29ebb08e5f0612)) 

### Features

* feat: enable use of other vocabularies ([`dd10ddb`](https://github.com/clnsmth/geoenvo/commit/dd10ddb8b6396de27dda6b44ac22cc373c0f2a50)) 

## v0.1.0 (2025-02-12)


### Bug fixes

* fix: SSSOM:NoMapping should not have a label ([`443d707`](https://github.com/clnsmth/geoenvo/commit/443d7070783b29fb626bb1e12bca79bbc9d6f885)) 
* fix: use get/set methods in attribute operations ([`796df4e`](https://github.com/clnsmth/geoenvo/commit/796df4ee3f8c74d0a781db8a8b033427fcb57b0a)) 
* fix: don't return useless SSSOM:NoMapping ([`62ba679`](https://github.com/clnsmth/geoenvo/commit/62ba679117fa0391b6443f9bda3d43223b689844)) 

### Features

* feat: add description to data model for context ([`4c2bce4`](https://github.com/clnsmth/geoenvo/commit/4c2bce4b63d7b35648ef29cfce6ed6f7bd3c4cee)) 
* feat: implement Schema.Org JSON-LD conversion of results ([`2d2f62c`](https://github.com/clnsmth/geoenvo/commit/2d2f62c3c9fc82fff4ea8c604f5ec6eb7d0f578b)) 
* feat: get and set class data with methods for protection ([`17175db`](https://github.com/clnsmth/geoenvo/commit/17175db60d03ebbd45fb445eededb3b0c81be591)) 

### Refactoring

* refactor: format for CI compliance ([`2afec6e`](https://github.com/clnsmth/geoenvo/commit/2afec6ef3bf61b30d525a6848a63dd1bd7f12313)) 
* refactor: update examples for user understanding ([`072e067`](https://github.com/clnsmth/geoenvo/commit/072e06722ce78353f720a2cbffddbffee4b2753b)) 
* refactor: format for CI compliance ([`2557472`](https://github.com/clnsmth/geoenvo/commit/2557472c375653f750ac5afcc2c787c0dd5e71bd)) 
* refactor: format recent code changes ([`cff6490`](https://github.com/clnsmth/geoenvo/commit/cff6490b3d33d2140fa0a980c6bd933c3b114e1f)) 

### Testing

* test: compare SchemaOrg output against fixture ([`0872115`](https://github.com/clnsmth/geoenvo/commit/08721152ca8044e7be6cb1580b9c47042211d7b6)) 

### Unknown

* Migrate code base from clnsmth/spinneret ([`9fb055d`](https://github.com/clnsmth/geoenvo/commit/9fb055d41af7f557a9727e80092048eb1cf0f289))


## v0.0.0 (2025-02-07)


### Unknown

* Initialize project repository ([`a76255f`](https://github.com/clnsmth/geoenvo/commit/a76255f745ad04bb42184a1b0861f0a7b78ab30d))
