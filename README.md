# Generate madelbrot iamges

## Parameters

1. Image-resolution-X
2. Image-resolution-Y 
3. X location of mandelbrot set
4. Y location of mandelbrot set
5. Zoom level (viewport of (-1,-1) to (1,1) is considered zoom level 1.0 )

## Examples
`./mandelbrot.py 1920 1080 0 0 0.75 > full.png # Full mandelbrot set in view`

`./mandelbrot.py 1920 1080 -0.75 0.1 50 > seahorses.png #Valley of seahorses`

## Notes
It runs with python3 as default, but I would strongly siuggest using pypy3 with Pillow since that really saves a lot of time.