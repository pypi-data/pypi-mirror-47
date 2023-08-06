# numbers_to_letters

Library for transform numbers int and float in text

# Use the library

Examples:

1. Example with int: 
   - import numbers_to_letters 
   - transform = numbers_to_letters.TransformNumbers()
   - number_to_letters = transform.number_to_letters(1200000)
   - 'UN MILLON DOSCIENTOS MIL'
 
2. Example with float:
- import numbers_to_letters 
   - transform = numbers_to_letters.TransformNumbers()
   - number_to_letters = transform.number_to_letters(1015421076.46, cents=True)
   - 'MIL QUINCE MILLONES CUATROCIENTOS VEINTI UN MIL SETENTA Y SEIS PUNTO CUARENTA Y SEIS'