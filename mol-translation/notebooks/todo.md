To Do


save labelled image
work out how many of each image we need. 9,999?

work out how to get inchi of mol with atoms we need

how to handle NH2s - 

```python
mol = Chem.MolFromSmiles("CCN")

editable = Chem.RWMol(mol)

# add H only to nitrogen atoms
for atom in editable.GetAtoms():
    if atom.GetSymbol() == "N":
        atom.SetNumExplicitHs(3)  # for amine-like nitrogen

mol2 = editable.GetMol()
```

or do something like add all h's then remove methyl ones (some of the time?)

```python
mol = Chem.AddHs(mol)

drawer = rdMolDraw2D.MolDraw2DCairo(300, 300)

opts = drawer.drawOptions()
opts.explicitMethylHydrogens = False  # cleaner default
```

save these per atom type in folders of 100?  C/0/0/01.png up to C/9/9/99.png


Need to do some bond stuff in the data set exploration bit
get bond coords
get bond type
