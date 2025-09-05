# Kodland-Tutor

# 🚀 Space Invaders - Pygame Edition

Un clon sencillo del clásico **Space Invaders**, desarrollado en **Python** usando **Pygame** y **Pygame-Menu**.  
El jugador controla una nave (Héroe) que dispara proyectiles para eliminar a los enemigos antes de que lleguen al borde inferior de la pantalla.

## 🎮 Características

- Menú inicial con selección de dificultad (**Fácil, Medio, Difícil**).
- Sistema de **vidas y puntuación**.
- Enemigos que bajan progresivamente por la pantalla.
- Límite de disparos activos en pantalla (máx. 5).
- Sistema de **vidas extra** cada 1000 puntos.
- Reinicio rápido con tecla `R` tras perder todas las vidas.
- Gráficos básicos con sprites personalizados.

## 📂 Estructura del Proyecto

```
📦 SpaceInvaders
 ┣ 📂 assets
 ┃ ┣ 🖼️ Heroe.png
 ┃ ┣ 🖼️ Enemigos.png
 ┃ ┗ 🖼️ Fondo.png
 ┣ 📜 main.py
 ┣ 📜 settings.py
 ┗ 📜 README.md
```

- **main.py** → Lógica principal del juego.  
- **settings.py** → Configuración (pantalla, colores, velocidad, sprites).  
- **assets/** → Carpeta con imágenes (Héroe, Enemigos, Fondo).  

## 🎹 Controles

- `←` o `A`: Mover héroe a la izquierda  
- `→` o `D`: Mover héroe a la derecha  
- `Espacio`: Disparar (máx. 5 balas activas)  
- `R`: Reiniciar partida (cuando aparezca **GAME OVER**)  
- `Esc`: Salir  

## 📊 Dificultades

- **Fácil** → Enemigos bajan lentamente.  
- **Medio** → Velocidad intermedia.  
- **Difícil** → Mayor velocidad de enemigos.  

## 🛠️ Requisitos

- Python **3.8+**
- Librerías:
  - `pygame`
  - `pygame-menu`

## 📌 Notas

Los sprites se cargan desde la carpeta `assets/`.  

- `Heroe.png`
- `Enemigos.png`
- `Fondo.png`

## 🏆 Autor

Desarrollado por **Jesús De Avila** ✨  
Proyecto educativo inspirado en el clásico **Space Invaders**.
