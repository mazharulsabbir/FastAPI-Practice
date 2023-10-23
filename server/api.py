from fastapi import FastAPI
import itertools

app = FastAPI(title='FastAPI-Practice')


@app.get("/")
async def root():
    attributes = {
        'color': ['Red', 'Blue', 'Green'],
        'size': ['Small', 'Medium', 'Large'],
        'material': ['Cotton', 'Polyester', 'Silk'],
    }

    # Generate all combinations of attribute values
    variant_combinations = list(itertools.product(*attributes.values()))

    # Create product variants as dictionaries
    product_variants = []
    for combination in variant_combinations:
        variant = {attribute: value for attribute, value in zip(attributes.keys(), combination)}
        product_variants.append(variant)

    return {"message": "Variants generated!!", "variants": product_variants}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
