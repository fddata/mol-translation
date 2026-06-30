from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from pathlib import Path

from PIL import Image
from io import BytesIO
from random import choice


def hello_world(input: str) -> str:
    return f"hello, world, {input}"


def _add_speckle(img: Image):
    arr = np.array(img)
    mask = np.random.random(arr.shape[:2])
    arr[mask < 0.003] = 0 # black noise
    arr[mask > 0.8] = 255 # white noise

    return Image.fromarray(arr)
    

def generate_labelled_images_from_inchi(
    
    inchi_list: list[str] = None,
    height: int = 350,
    width: int = 350,
    box_size: int = 18,
    target_atom: str = None,
    save_path: str = None,
    target_image_count: int = 0
):

    if not inchi_list:
        raise ValueError("need valid InChI value")

    if not save_path:
        raise ValueError("need valid save_path value")

    if not target_atom:
        raise ValueError("need valid target_atom")
    

    counter = 0

    while counter < target_image_count:

        for inchi in inchi_list:

            mol = Chem.MolFromInchi(inchi)
            AllChem.Compute2DCoords(mol)
            drawer = Draw.rdMolDraw2D.MolDraw2DCairo(height, width)
        
            opts = drawer.drawOptions()
            opts.useBWAtomPalette()
            opts.rotate = choice(range(360))
            opts.bondLineWidth = choice([0.75, 1])
            opts.fixedFontSize = choice(range(12,18))
            # drawer.SetFontSize(40.0)
        
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()
            
            img_bytes = drawer.GetDrawingText()
            img_pil = Image.open(BytesIO(img_bytes))
            img_pil.load() # force into memory to prevent Jupyter renering hangs
            img_pil = _add_speckle(img_pil)
            img_pil.show()

            save_dir = Path(save_path)
            save_dir.mkdir(parents=True, exist_ok=True)
        
            # ImageOps.expand(img_pil, border = int(box_size/2), fill="white")
        
            for atom in mol.GetAtoms():

                if counter % 10 == 0:
                    print (f"Processing image {counter} of {target_image_count}")
        
                # print(f"{atom.GetSymbol()}_{atom.GetIdx()}.png")
                pt = drawer.GetDrawCoords(atom.GetIdx())
                x = pt.x
                y = pt.y
            
                xmin = max(0, x - box_size)
                ymin = max(0, y - box_size)
                xmax = min(width, x + box_size)
                ymax = min(height, y + box_size)
        
                cropped = img_pil.crop((xmin, ymin, xmax, ymax))
                cropped.load()
                cropped = add_speckle(cropped)
            
                cropped.save(Path(save_path +  f"/{atom.GetSymbol()}/{atom.GetSymbol()}_{atom.GetIdx()}.png"))
                cropped.close()

                counter += 1 
        
            img_pil.close()

    
        