# VR, AR & Haptics Exam Answers

Short bilingual notes for quick revision.

Format:
- EN: simple B2-level exam answer.
- RU: same idea in Russian.

---

## 1. What is a GameObject in Unity?

EN: A GameObject is the basic object in a Unity scene. By itself it is only a container. Its behavior and appearance come from Components, such as Transform, Mesh Renderer, Collider, Rigidbody, Camera, or custom C# scripts.

RU: GameObject - базовый объект сцены Unity. Сам по себе он является контейнером. Его внешний вид и поведение задаются компонентами: Transform, Mesh Renderer, Collider, Rigidbody, Camera или пользовательскими C# скриптами.

## 2. What is a Component?

EN: A Component is a module attached to a GameObject. Components add data and behavior. For example, Transform stores position, rotation, and scale; Rigidbody adds physics; Collider defines the physical shape; scripts define custom logic.

RU: Component - модуль, прикрепленный к GameObject. Компоненты добавляют данные и поведение. Например, Transform хранит позицию, поворот и масштаб, Rigidbody добавляет физику, Collider задает форму столкновений, скрипты задают свою логику.

## 3. What is Transform?

EN: Transform is a required component of every GameObject. It stores position, rotation, and scale in the scene. It also defines parent-child hierarchy, so child objects move relative to their parent.

RU: Transform - обязательный компонент каждого GameObject. Он хранит позицию, поворот и масштаб. Также Transform задает иерархию parent-child, поэтому дочерние объекты двигаются относительно родителя.

## 4. What is the difference between Update and FixedUpdate?

EN: Update is called once per rendered frame, so it is good for reading input and non-physics logic. FixedUpdate is called at a fixed time step and is used for physics, for example Rigidbody movement and AddForce.

RU: Update вызывается один раз на каждый отображаемый кадр, поэтому подходит для чтения ввода и обычной логики. FixedUpdate вызывается с фиксированным шагом времени и используется для физики, например Rigidbody и AddForce.

## 5. Why do we use GetComponent<T>()?

EN: GetComponent<T>() is used to access another component on the same GameObject. For example, a movement script can get a Rigidbody in Start and then use it later to apply forces.

RU: GetComponent<T>() используется, чтобы получить доступ к компоненту на том же GameObject. Например, скрипт движения может получить Rigidbody в Start, а потом применять к нему силы.

## 6. What is a Rigidbody?

EN: Rigidbody is a physics component. It allows a GameObject to be affected by gravity, forces, velocity, and collisions. If an object should move physically, it usually needs a Rigidbody.

RU: Rigidbody - физический компонент. Он позволяет объекту реагировать на гравитацию, силы, скорость и столкновения. Если объект должен физически двигаться, ему обычно нужен Rigidbody.

## 7. What is a Collider?

EN: A Collider defines the physical shape used for collisions and triggers. It does not need to match the visible mesh exactly. Common colliders are Box, Sphere, Capsule, and Mesh Collider.

RU: Collider задает физическую форму для столкновений и триггеров. Он не обязан точно совпадать с видимой моделью. Частые типы: Box, Sphere, Capsule и Mesh Collider.

## 8. Static, Kinematic, and Dynamic objects

EN: Static objects are environment objects that do not move. Kinematic objects are moved by scripts or animation, not by forces. Dynamic objects are controlled by physics: gravity, forces, collisions, and Rigidbody simulation.

RU: Static объекты - неподвижное окружение. Kinematic объекты двигаются скриптом или анимацией, а не силами. Dynamic объекты управляются физикой: гравитацией, силами, столкновениями и Rigidbody.

## 9. Collision vs Trigger

EN: A collision happens when non-trigger colliders physically touch, usually with at least one Rigidbody. Objects can bounce or push each other. A trigger detects overlap without physical response, so objects can pass through it.

RU: Collision происходит, когда обычные коллайдеры физически соприкасаются, обычно с хотя бы одним Rigidbody. Объекты могут толкаться или отскакивать. Trigger только обнаруживает пересечение без физической реакции.

## 10. Collision event methods

EN: Unity uses OnCollisionEnter, OnCollisionStay, and OnCollisionExit for physical collisions. They receive a Collision object, which contains information about contacts, the other object, and collision details.

RU: Для физических столкновений Unity использует OnCollisionEnter, OnCollisionStay и OnCollisionExit. Они получают объект Collision с информацией о контактах, другом объекте и деталях столкновения.

## 11. Trigger event methods

EN: Unity uses OnTriggerEnter, OnTriggerStay, and OnTriggerExit for trigger zones. They receive the other Collider. Triggers are useful for pickup zones, checkpoints, placement zones, and detection areas.

RU: Для триггерных зон Unity использует OnTriggerEnter, OnTriggerStay и OnTriggerExit. Они получают другой Collider. Триггеры полезны для зон подбора, чекпоинтов, зон размещения и областей обнаружения.

## 12. Primitive colliders vs Mesh colliders

EN: Primitive colliders, such as box, sphere, and capsule, are simple and fast. Mesh colliders use the real mesh shape, so they are more accurate but slower. For performance, simple colliders are preferred when possible.

RU: Примитивные коллайдеры, например box, sphere и capsule, простые и быстрые. Mesh Collider использует форму модели, он точнее, но медленнее. Для производительности лучше использовать простые коллайдеры, если это возможно.

## 13. Convex and non-convex Mesh Collider

EN: A convex Mesh Collider uses a simplified hull around the object. It is required for dynamic or kinematic Rigidbody objects that use mesh colliders. Non-convex mesh colliders are mainly for static environment geometry.

RU: Convex Mesh Collider использует упрощенную оболочку вокруг объекта. Он нужен для dynamic или kinematic Rigidbody с mesh collider. Non-convex mesh collider обычно используется для статического окружения.

## 14. AddForce

EN: AddForce applies a force to a Rigidbody. It is usually called in FixedUpdate. It is useful for physics-based movement, where the object accelerates naturally instead of changing position directly.

RU: AddForce применяет силу к Rigidbody. Обычно вызывается в FixedUpdate. Это удобно для физического движения, когда объект естественно ускоряется, а не просто меняет позицию напрямую.

## 15. AddRelativeForce

EN: AddRelativeForce applies force in the local coordinate system of the object. For example, forward force means the object's own forward direction, not the world's forward direction.

RU: AddRelativeForce применяет силу в локальной системе координат объекта. Например, forward означает собственное направление объекта вперед, а не глобальное направление мира.

## 16. ForceMode.Force

EN: ForceMode.Force applies continuous force over time and uses the object's mass. It is good for engines, pushing, or gradual acceleration.

RU: ForceMode.Force применяет постоянную силу во времени и учитывает массу объекта. Подходит для двигателей, толкания и постепенного ускорения.

## 17. ForceMode.Acceleration

EN: ForceMode.Acceleration applies continuous acceleration and ignores mass. Objects with different mass accelerate in the same way.

RU: ForceMode.Acceleration применяет постоянное ускорение и не учитывает массу. Объекты с разной массой ускоряются одинаково.

## 18. ForceMode.Impulse

EN: ForceMode.Impulse applies an instant force and uses mass. It is useful for jumps, explosions, hits, or sudden pushes.

RU: ForceMode.Impulse применяет мгновенный импульс и учитывает массу. Используется для прыжков, взрывов, ударов и резкого толчка.

## 19. ForceMode.VelocityChange

EN: ForceMode.VelocityChange changes velocity instantly and ignores mass. It is useful when we want the same instant speed change for all objects.

RU: ForceMode.VelocityChange мгновенно меняет скорость и не учитывает массу. Полезно, когда всем объектам нужно дать одинаковое изменение скорости.

## 20. New Input System

EN: Unity's New Input System is a flexible way to handle keyboard, mouse, gamepad, touch, and XR input. It uses Input Actions instead of hard-coded input checks.

RU: New Input System в Unity - гибкая система ввода для клавиатуры, мыши, геймпада, touch и XR. Она использует Input Actions вместо жестко прописанных проверок кнопок.

## 21. Action Maps, Actions, and Bindings

EN: An Action Map groups actions for a context, for example Player. An Action is a logical input, for example Move or Interact. A Binding connects that action to real controls, for example WASD or mouse click.

RU: Action Map группирует действия для контекста, например Player. Action - логический ввод, например Move или Interact. Binding связывает action с реальными кнопками, например WASD или click мыши.

## 22. Reading input in script

EN: After generating the C# class, we create an instance of it, enable the action map, and read values. Example: Move.ReadValue<Vector2>() or Move.ReadValue<Vector3>(). Actions should be disabled in OnDisable.

RU: После генерации C# класса создается его экземпляр, включается action map и читаются значения. Например: Move.ReadValue<Vector2>() или Move.ReadValue<Vector3>(). В OnDisable actions лучше отключать.

## 23. Why read input in Update and apply physics in FixedUpdate?

EN: Input is frame-based, so Update is the best place to read it. Physics is calculated at fixed time steps, so Rigidbody forces should be applied in FixedUpdate for stable behavior.

RU: Ввод зависит от кадров, поэтому его удобно читать в Update. Физика считается с фиксированным шагом, поэтому силы Rigidbody лучше применять в FixedUpdate для стабильного поведения.

## 24. Raycasting

EN: Raycasting sends an invisible ray from an origin in a direction and checks what collider it hits. It is used for mouse picking, aiming, line of sight, object selection, and interaction.

RU: Raycasting выпускает невидимый луч из точки в заданном направлении и проверяет, какой collider он задел. Используется для выбора объектов мышью, прицеливания, проверки видимости и интеракции.

## 25. RaycastHit

EN: RaycastHit stores information about a raycast result: the hit collider, hit point, distance, normal, and object transform. It is filled by Physics.Raycast when the ray hits something.

RU: RaycastHit хранит результат raycast: задетый collider, точку попадания, расстояние, нормаль и transform объекта. Он заполняется Physics.Raycast, если луч во что-то попал.

## 26. Tags

EN: Tags are text labels used to identify GameObjects in logic. For example, an object can have the tag Collectible or PlacementZone. In scripts we can check tags with CompareTag.

RU: Tags - текстовые метки для идентификации GameObject в логике. Например, объект может иметь tag Collectible или PlacementZone. В коде теги проверяют через CompareTag.

## 27. Layers

EN: Layers are used to group objects for physics, rendering, and selection. They can control which objects collide and which objects are included in raycasts or camera rendering.

RU: Layers группируют объекты для физики, рендера и выбора. С их помощью можно управлять тем, какие объекты сталкиваются, попадают в raycast или видны камере.

## 28. LayerMask

EN: LayerMask tells Unity which layers should be included or ignored in an operation. For example, Physics.Raycast can receive a LayerMask so it only hits Interactable objects.

RU: LayerMask сообщает Unity, какие слои учитывать или игнорировать. Например, Physics.Raycast может получить LayerMask и попадать только по объектам слоя Interactable.

## 29. Layer Collision Matrix

EN: The Layer Collision Matrix controls which layers can collide with each other. It improves performance and avoids unwanted collisions, for example Player not colliding with PlayerSensor.

RU: Layer Collision Matrix задает, какие слои могут сталкиваться друг с другом. Это улучшает производительность и убирает нежелательные столкновения, например Player с PlayerSensor.

## 30. Raycast, RaycastAll, SphereCast, BoxCast

EN: Raycast checks a thin line and returns the first hit. RaycastAll returns all hits along the ray. SphereCast sweeps a sphere through space. BoxCast sweeps a box. Casts with volume are useful for wider detection.

RU: Raycast проверяет тонкий луч и возвращает первое попадание. RaycastAll возвращает все попадания вдоль луча. SphereCast двигает сферу, BoxCast двигает коробку. Объемные casts полезны для широкой проверки.

## 31. Prefab

EN: A Prefab is a reusable GameObject asset. It stores components, children, and settings. Changes to the prefab can update all its instances, which helps keep objects consistent.

RU: Prefab - переиспользуемый GameObject asset. Он хранит компоненты, дочерние объекты и настройки. Изменения prefab могут обновить все его экземпляры, что помогает сохранять консистентность.

## 32. Prefab variants and nested prefabs

EN: A prefab variant inherits from a base prefab but can have overrides. A nested prefab is a prefab placed inside another prefab. They help organize related objects, such as a car with wheel prefabs.

RU: Prefab variant наследуется от базового prefab, но может иметь свои изменения. Nested prefab - prefab внутри другого prefab. Это удобно для связанных объектов, например машина с prefab колесами.

## 33. Canvas

EN: Canvas is the root object for Unity UI. UI elements such as Text, Button, Panel, Slider, Dropdown, and Input Field must be placed under a Canvas to be rendered.

RU: Canvas - корневой объект для UI в Unity. UI элементы, такие как Text, Button, Panel, Slider, Dropdown и Input Field, должны находиться внутри Canvas, чтобы отображаться.

## 34. Canvas render modes

EN: Screen Space Overlay draws UI over everything on the screen. Screen Space Camera renders UI through a selected camera. World Space makes UI exist as a 3D object in the scene, useful for VR.

RU: Screen Space Overlay рисует UI поверх всего экрана. Screen Space Camera отображает UI через выбранную камеру. World Space делает UI 3D объектом в сцене, что полезно для VR.

## 35. TextMeshPro

EN: TextMeshPro is Unity's advanced text system. It provides better quality, styling, and control than the old UI Text. It is commonly used for readable UI labels and status text.

RU: TextMeshPro - продвинутая система текста в Unity. Она дает лучшее качество, стилизацию и контроль, чем старый UI Text. Часто используется для читаемых UI надписей и статусов.

## 36. Button OnClick event

EN: A Button has an OnClick event list. We add a listener, drag a GameObject with a script into the slot, and choose a public method from the dropdown. The method is called when the button is clicked.

RU: У Button есть список событий OnClick. Мы добавляем listener, перетаскиваем GameObject со скриптом в слот и выбираем public метод из dropdown. Метод вызывается при нажатии кнопки.

## 37. Reset scene with SceneManager

EN: To reset a scene, use SceneManager.LoadScene with the current scene name. We need using UnityEngine.SceneManagement. The scene must also be added to Build Settings.

RU: Чтобы перезапустить сцену, используют SceneManager.LoadScene с именем текущей сцены. Нужно подключить using UnityEngine.SceneManagement. Сцена также должна быть добавлена в Build Settings.

## 38. XR, VR, AR, MR

EN: XR is an umbrella term for extended reality. VR is a fully virtual environment. AR overlays digital content on the real world. MR mixes real and virtual objects so they can interact in real time.

RU: XR - общий термин для extended reality. VR - полностью виртуальная среда. AR накладывает цифровой контент на реальный мир. MR смешивает реальные и виртуальные объекты с взаимодействием в реальном времени.

## 39. VR application areas

EN: VR is used in training, education, robotics, teleoperation, medicine, design, architecture, entertainment, data visualization, and simulation of dangerous or expensive scenarios.

RU: VR используется в обучении, образовании, робототехнике, телеоперации, медицине, дизайне, архитектуре, развлечениях, визуализации данных и симуляции опасных или дорогих сценариев.

## 40. VR advantages and disadvantages

EN: Advantages include immersion, safe training, high engagement, realistic simulation, and lower risk. Disadvantages include high cost, technical complexity, motion sickness, physical discomfort, and possible psychological effects.

RU: Преимущества: погружение, безопасное обучение, высокая вовлеченность, реалистичная симуляция и снижение риска. Недостатки: высокая стоимость, техническая сложность, motion sickness, физический дискомфорт и возможные психологические эффекты.

## 41. Motion sickness and teleportation

EN: Motion sickness happens when visual motion does not match the body's vestibular feeling. Teleportation reduces this problem because the user changes position instantly instead of moving smoothly through virtual space.

RU: Motion sickness возникает, когда визуальное движение не совпадает с ощущениями вестибулярной системы. Teleportation уменьшает проблему, потому что пользователь мгновенно меняет позицию, а не плавно движется в VR.

## 42. XR Interaction Toolkit

EN: XR Interaction Toolkit is a Unity package for VR and AR interactions. It provides cross-device input, locomotion, teleportation, grabbing, sockets, ray interaction, direct interaction, gaze, and world-space UI support.

RU: XR Interaction Toolkit - пакет Unity для VR и AR взаимодействий. Он дает cross-device input, locomotion, teleportation, grabbing, sockets, ray/direct interaction, gaze и поддержку world-space UI.

## 43. XR Origin

EN: XR Origin represents the player's physical play space and XR hardware in the Unity scene. It usually contains Camera Offset, Main Camera, and left and right controller objects.

RU: XR Origin представляет физическое пространство игрока и XR оборудование в сцене Unity. Обычно содержит Camera Offset, Main Camera и объекты левого и правого контроллеров.

## 44. XR Device Simulator

EN: XR Device Simulator lets developers test XR input with keyboard and mouse without a real headset. It can simulate headset and controller movement, which is useful for development and debugging.

RU: XR Device Simulator позволяет тестировать XR ввод клавиатурой и мышью без реального шлема. Он симулирует движение headset и контроллеров, что удобно для разработки и отладки.

## 45. XR Grab Interactable

EN: XR Grab Interactable is a component for objects that can be picked up in VR. It works with XR Ray Interactor or XR Direct Interactor. Movement Type controls how the object follows the hand.

RU: XR Grab Interactable - компонент для объектов, которые можно брать в VR. Он работает с XR Ray Interactor или XR Direct Interactor. Movement Type задает, как объект следует за рукой.

## 46. Grab movement types

EN: Instantaneous makes the object snap to the hand immediately. Kinematic moves it smoothly and ignores most physics forces. Velocity Tracking is physics-based, so the object has weight, momentum, and natural throwing.

RU: Instantaneous мгновенно переносит объект к руке. Kinematic двигает его плавно и почти игнорирует физику. Velocity Tracking основан на физике, поэтому объект имеет вес, импульс и естественный бросок.

## 47. Ray Interactor vs Direct Interactor

EN: XR Ray Interactor allows interaction from a distance using a ray, like a laser pointer. XR Direct Interactor allows interaction by touching objects with the controller. Ray is good for far UI; direct is good for hands-on grabbing.

RU: XR Ray Interactor позволяет взаимодействовать на расстоянии лучом, как лазерной указкой. XR Direct Interactor работает при касании объекта контроллером. Ray удобен для дальнего UI, Direct - для ручного захвата.

## 48. XR Socket Interactor

EN: XR Socket Interactor is a placement point that can hold interactable objects. It can use Interaction Layer Mask to accept only specific objects, for example only a blue cube in a matching socket.

RU: XR Socket Interactor - точка размещения, которая может удерживать interactable объекты. Через Interaction Layer Mask можно принимать только определенные объекты, например только синий куб в нужный socket.

## 49. AR and AR tracking

EN: AR overlays digital content on the real world. Marker-based tracking recognizes predefined images or objects and is accurate but limited. SLAM or ground-plane tracking maps the environment without markers. Hybrid tracking combines both.

RU: AR накладывает цифровой контент на реальный мир. Marker-based tracking распознает заранее заданные изображения или объекты, он точный, но ограниченный. SLAM/ground-plane tracking строит карту среды без маркеров. Hybrid tracking объединяет оба подхода.

## 50. Vuforia and Image Targets

EN: Vuforia is an AR SDK that integrates with Unity. Image Targets are 2D images recognized by Vuforia. Good targets have many unique feature points, high contrast, rich detail, and non-repetitive patterns.

RU: Vuforia - AR SDK, который интегрируется с Unity. Image Targets - 2D изображения, которые распознает Vuforia. Хорошие target имеют много уникальных feature points, высокий контраст, богатые детали и неповторяющиеся паттерны.

## 51. Vuforia target database

EN: In Vuforia Developer Portal, we create a database, add an image target, enter its real physical width, and download the Unity package. Then we import it into Unity and assign it to an ImageTarget GameObject.

RU: В Vuforia Developer Portal создают database, добавляют image target, указывают его реальную физическую ширину и скачивают Unity package. Затем его импортируют в Unity и назначают ImageTarget GameObject.

## 52. Feature points and target quality

EN: Vuforia does not simply compare the whole image. It extracts feature points such as corners, high-contrast areas, and textured details. A 4-5 star target is usually reliable; blurry, symmetric, or repetitive images are bad.

RU: Vuforia не просто сравнивает всю картинку. Она извлекает feature points: углы, контрастные области и текстурные детали. Target на 4-5 звезд обычно надежный; размытые, симметричные или повторяющиеся изображения плохие.

## 53. Anchoring content to ImageTarget

EN: To anchor content, make the 3D object a child of the ImageTarget. Then it appears, disappears, moves, and rotates together with the physical target. Its position and scale are relative to the target size.

RU: Чтобы закрепить контент, нужно сделать 3D объект дочерним объектом ImageTarget. Тогда он появляется, исчезает, двигается и вращается вместе с физическим target. Его позиция и масштаб считаются относительно размера target.

## 54. Tracking found and lost events

EN: Vuforia can notify when a target is found or lost. DefaultObserverEventHandler provides events such as On Target Found and On Target Lost. We can use them to show or hide content or update UI status.

RU: Vuforia может сообщать, когда target найден или потерян. DefaultObserverEventHandler дает события On Target Found и On Target Lost. Их можно использовать, чтобы показывать/скрывать контент или обновлять UI статус.

## 55. AR build settings

EN: For Android AR, common settings are ARM64 architecture, IL2CPP scripting backend, camera permission, and a valid package name. For iOS, use ARM64, IL2CPP, camera usage description, and build through Xcode on a real device.

RU: Для Android AR часто нужны ARM64, IL2CPP scripting backend, разрешение камеры и корректный package name. Для iOS нужны ARM64, IL2CPP, camera usage description и сборка через Xcode на реальное устройство.

---

# Very Short Cheat Sheet

EN:
- GameObject = container; Component = behavior/data.
- Rigidbody = physics body; Collider = physical shape.
- Collision = physical contact; Trigger = overlap detection.
- Update = input/frame logic; FixedUpdate = physics.
- Raycast = invisible line for detection.
- Tag = label; Layer = filtering group; LayerMask = choose layers.
- Prefab = reusable object template.
- Canvas = UI root; World Space Canvas is useful in VR.
- XR = VR + AR + MR.
- XR Origin = player rig; XRI = ready-made XR interaction tools.
- Teleportation helps reduce motion sickness.
- AR = digital content over real world.
- Vuforia Image Target = recognized 2D marker.
- Good target = many unique feature points.
- Anchoring = make content child of ImageTarget.

RU:
- GameObject = контейнер; Component = поведение/данные.
- Rigidbody = физическое тело; Collider = физическая форма.
- Collision = физический контакт; Trigger = обнаружение пересечения.
- Update = ввод/логика по кадрам; FixedUpdate = физика.
- Raycast = невидимый луч для обнаружения.
- Tag = метка; Layer = группа фильтрации; LayerMask = выбор слоев.
- Prefab = переиспользуемый шаблон объекта.
- Canvas = корень UI; World Space Canvas полезен в VR.
- XR = VR + AR + MR.
- XR Origin = rig игрока; XRI = готовые инструменты XR взаимодействия.
- Teleportation уменьшает motion sickness.
- AR = цифровой контент поверх реального мира.
- Vuforia Image Target = распознаваемый 2D маркер.
- Хороший target = много уникальных feature points.
- Anchoring = сделать контент дочерним объектом ImageTarget.
