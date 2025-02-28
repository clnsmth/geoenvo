
# CHANGELOG



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
