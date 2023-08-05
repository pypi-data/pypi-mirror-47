`pulm`: PlantUML script generator
=================================

## Getting started

As an example we can use `pulm` on its own code.


```bash
$ git clone
$ cd pulm
$ python setup.py
$ pulm ./pulm/pulm.py | plantuml -p > out/pulm.png && open out/pulm.png
```
_et voilà_.

![pulm class diagramm](./docs/pulm.png)

You can do some more magic with `entr` to generate UML diagram on the fly 🛩

## License

[This project license](./LICENSE) is MIT.
