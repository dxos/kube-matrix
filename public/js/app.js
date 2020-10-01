const ns = 'http://www.w3.org/2000/svg';
const ws = new WebSocket(`wss://${window.location.host}`);

class LedArray {
  constructor(svg, width, height) {
    this.svg = svg;
    this.width = width;
    this.height = height;

    this.pixels = [];

    const size = 40;
    const spacing = 500 / 11;

    for (let y = 0; y < height; y++) {
      const row = [];

      for (let x = 0; x < width; x++) {
        row.push(0);

        const square = document.createElementNS(ns, 'rect');
        square.setAttribute('width', size);
        square.setAttribute('height', size);

        square.setAttribute('x', x * spacing);
        square.setAttribute('y', y * spacing);

        square.setAttribute('stroke', 'black');
        square.setAttribute('fill', 'white');

        square.setAttribute('id', `${x},${y}`);

        svg.appendChild(square);
      }

      this.pixels.push(row);
    }
  }

  set(x, y, r, g, b) {
    if (x < 0 || x > this.width || y < 0 || y > this.height) {
      throw new Error('Out of bounds');
    }

    this.pixels[y][x] = [r, g, b];
  }

  render() {
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const [r, g, b] = this.pixels[y][x];
        const pxEl = svg.getElementById(`${x},${y}`);
        pxEl.setAttribute('fill', `rgb(${r},${g},${b})`);
      }
    }
  }
}

const svg = document.getElementById('leds');
const leds = new LedArray(svg, 11, 11);

function shadePlasma(iteration, x, y) {
  const t = iteration / 100.0;

  const r = 127 * (1 + Math.cos(t + 0.1 * x));
  const g = 127 * (1 + Math.sin(t + 0.3 * y));
  const b = 127;

  return [r, g, b];
}

let time = 0;
function render() {
  for (let y = 0; y < leds.height; y++) {
    for (let x = 0; x < leds.width; x++) {
      const [r, g, b] = shadePlasma(time, x, y);
      leds.set(x, y, r, g, b);
    }
  }

  time += 1;

  leds.render();

  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(leds.pixels));
  }

  requestAnimationFrame(render);
}

render();
