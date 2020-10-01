const ns = 'http://www.w3.org/2000/svg';
const ws = new WebSocket(`wss://${window.location.host}`);

let mouseX = 0;
let mouseY = 0;

function dist(x1, y1, x2, y2) {
  return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}

function constrain(v, min, max) {
  return Math.min(Math.max(v, 0), 255);
}

function lerp(start, end, ratio) {
  return start + (end - start) * ratio;
}

class LedArray {
  constructor(svg, width, height) {
    this.svg = svg;
    this.width = width;
    this.height = height;

		document.onmousemove = (event) => {
			const rect = this.svg.getBoundingClientRect();

			mouseX = this.width * (event.clientX - rect.x) / rect.width;
			mouseY = this.height * (event.clientY - rect.y) / rect.height;

			console.log(mouseX, mouseY);
		};

    this.pixels = [];

    const size = 40;
    const spacing = 500 / 11;

    for (let y = 0; y < height; y++) {
      const row = [];

      for (let x = 0; x < width; x++) {
        row.push([0, 0, 0, 0]);

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

  set(x, y, r, g, b, a) {
    if (x < 0 || x > this.width || y < 0 || y > this.height) {
      throw new Error('Out of bounds');
    }

    this.pixels[y][x] = [r, g, b, a]
      .map(Math.floor)
      .map(v => Math.min(Math.max(v, 0), 255));
  }

  render() {
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const [r, g, b, a] = this.pixels[y][x];

        const rc = constrain(r + a, 0, 255);
        const gc = constrain(g + a, 0, 255);
        const bc = constrain(b + a, 0, 255);

        const pxEl = svg.getElementById(`${x},${y}`);
        pxEl.setAttribute('fill', `rgb(${rc},${gc},${bc})`);
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
  const a = 0;

  return [r, g, b, a];
}

function shadeBreathing(iteration, x, y) {
  const t = iteration / 10.0;

  const r = 0;
  const g = 0;
  const b = 0;
  const a = 127 * (1 + Math.sin(t));

  return [r, g, b, a];
}

function shadeRotatingCircle(iteration, x, y) {
  const t = iteration / 10.0;

  const cx = 5.5;
  const cy = 5.5;

  const radius = 2;
  const ex = cx + radius * Math.cos(t);
  const ey = cy + radius * Math.sin(t);

  const r = 0;
  const g = 0;
  const b = 0;
  const a = lerp(0, 255, (3 - dist(x, y, ex, ey)) / 3);

  return [r, g, b, a];
}

function shadeMousePosition(iteration, x, y) {
  const t = iteration / 10.0;

  const cx = 5.5;
  const cy = 5.5;

  const radius = 2;
  const ex = mouseX;
  const ey = mouseY;

  const r = 0;
  const g = 0;
  const b = 0;
  const a = lerp(0, 255, (3 - dist(x, y, ex, ey)) / 3);

  return [r, g, b, a];
}

const shadeNetwork = (() => {
  const nodes = [];

  for (let i = 0; i < 4; i++) {
    nodes.push([Math.random() * 11, Math.random() * 11]);
  }

  return (iteration, x, y) => {
    const minDist = nodes.reduce((d, [nx, ny]) => {
      const thisDist = dist(x, y, nx, ny);
      return thisDist < d ? thisDist : d;
    }, Infinity);;

    const radius = 
    
    const r = 0;
    const g = 0;
    const b = 0;
    const a = minDist < radius ? 64 : 0;
    //constrain(255 * lerp(1, 0, minDist / 11), 0, 255);

    return [r, g, b, a];
  };
})();

let time = 0;
function render() {
  for (let y = 0; y < leds.height; y++) {
    for (let x = 0; x < leds.width; x++) {
      const [r, g, b, a] = shadeNetwork(time, x, y);
      leds.set(x, y, r, g, b, a);
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
