# Marble Input Selection Notes

## Selection criteria
- Use selected edited/reference car images when available, not raw
  car photos, because Marble should test the downstream consumer visualization
  condition.
- Prefer full-car images with the target car large in frame.
- Prefer clear visibility of both visible wheels and the edited rim design.
- Prefer daylight or evenly lit scenes over night images.
- Avoid strong occlusions, tiny cars, crowds, and complex traffic scenes.
- Blur readable plates in selected copies before public use.

## Selected pilot inputs
- `car_01.png`: front three-quarter white SUV. Best hero-style input and useful
  for testing whether Marble preserves frontal design and black rims.
- `car_02.png`: side-view hatchback. Clean geometry, both wheels visible, dirt
  marks provide extra identity cues.
- `car_03.png`: side-view wagon. Distinct silhouette and dark wheels.
- `car_04.png`: side-view large SUV. Strong wheel visibility and different body
  class from the smaller cars.

## Backups
- `reve-v1.1 C4 R3.png`: good rear three-quarter SUV, but readable rear plate
  should be blurred before use.
- `Generated Images/dream-wheels-cfa3bad7-45c7-4be8-be26-ef52fa1306a6.jpg`:
  clean front three-quarter generated result, but less directly tied to the
  Ivan RESULTADOS set and has visible plate branding.
- `Generated Images/photo_2026-04-14 14.12.43.jpeg`: clear red car with visible
  wheels, but the source looks more internet/listing-like and has plate text.

## GPT Image note
If OpenAI GPT Image produces stronger wheel-replacement results, keep the same
selection criteria and replace only one or two pilot inputs. Do not mix many
generation methods in the same primary pilot unless the condition label records
the source model.
