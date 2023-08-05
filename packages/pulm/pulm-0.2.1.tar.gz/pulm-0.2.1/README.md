`pulm`: PlantUML script generator
=================================

## Installing `pulm`

You can install it from Pypi:
```bash
pip install pulm
```

You can directly install it from source too:
```bash
$ git clone python git@github.com:jjerphan/pulm.git
$ cd pulm
$ python setup.py install
```

## Usage

As an example we can use `pulm` on its own code.

```bash
$ pulm ./pulm/pulm.py | plantuml -p > out/pulm.png && open out/pulm.png
```
_et voilà_.

![pulm class diagramm](./docs/pulm.png)

You can do some more magic with `entr` to generate UML diagram on the fly 🛩

## License

[This project license](./LICENSE) is MIT.
