# pdb_to_lt_oplsaa
This is the python script (experimentally) for generate .lt file that inherit OPLS-AA force field from .pdb file to be use in moltemplate.

I made this to automatically generate the .lt file, you can also generate it manually following Moltemplate Documentation (https://github.com/jewettaij/moltemplate/tree/master/moltemplate/force_fields/build_your_own_force_field)

To use the script, simply use this command:
```
python3 pdb_to_lt_oplsaa.py molecule.pdb MoleculeName
```
You can see the example in the example folder.

Basically, you can convert any PDB file and generate .lt that inherits OPLS-AA force field using this script. But this script is still in experimentally phase, so if you encounter any error when you're running moltemplate using the file that geenrated from this script feel free to report it.
