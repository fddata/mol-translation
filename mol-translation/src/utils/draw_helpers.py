from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from pathlib import Path
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')


from PIL import Image
from io import BytesIO
from random import choice
import numpy as np
from pathlib import Path


def _add_speckle(img: Image):
    arr = np.array(img)
    mask = np.random.random(arr.shape[:2])
    arr[mask < 0.003] = 0 # black noise
    arr[mask > 0.8] = 255 # white noise

    return Image.fromarray(arr)

    
def _get_save_path(counter: int = None, symbol: str = None) -> str:
    "calculates relative path for saving a training image"

    if not 0 <= counter <= 99_999:
        raise ValueError(f"counter should be between 0 and 99,999, found: {counter}")

    l1 = str(counter // 1000).zfill(2)
    filename = f"{symbol}_{str(counter).zfill(5)}.png"
    return f"{symbol}/{l1}/{filename}"


def _save_image(image, prefix_path, save_path: str):

    full_path = Path(prefix_path) / save_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(full_path)


def generate_labelled_images_from_inchi(
    inchi_list: list[str] = None,
    height: int = 350,
    width: int = 350,
    box_size: int = 18,
    target_atom: str = None,
    save_path_prefix: str = "../data/images/train_synthetic/", # assumes called from notebooks/ folder
    target_image_count: int = 0
):


    if not inchi_list:
        raise ValueError("need valid InChI value")

    if not save_path_prefix:
        raise ValueError("need valid save_path_prefix value")

    if not target_atom:
        raise ValueError("need valid target_atom")
    
    counter = 0

    print(f"Processing {target_image_count} images for element: {target_atom}")
    
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
            
            for atom in mol.GetAtoms():
                symbol = atom.GetSymbol()
                
                if symbol != target_atom:
                    continue

                if counter % 500 == 0:
                    print (f"Processing {symbol} image {counter} of {target_image_count}")
        
                pt = drawer.GetDrawCoords(atom.GetIdx())
                x = pt.x
                y = pt.y
            
                xmin = max(0, x - box_size)
                ymin = max(0, y - box_size)
                xmax = min(width, x + box_size)
                ymax = min(height, y + box_size)
        
                cropped = img_pil.crop((xmin, ymin, xmax, ymax))
                cropped.load()

                save_path = _get_save_path(counter, symbol)
                _save_image(cropped, save_path_prefix, save_path)
                
                cropped.close()

                counter += 1
        
            img_pil.close()
