//
// Test client (communicates via WSS to the Node server).
// Runs in the browser to leverage the canvas API.
//

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
  const t = iteration / 10.0;

  const r = 127 * (1 + Math.cos(t + 0.1 * x));
  const g = 127 * (1 + Math.sin(0.3 * t + 0.35 * y));
  const b = 127;
  const a = 0;

  return [r, g, b, a];
}

function shadeBreathing(iteration, x, y) {
  const t = iteration / 100.0;

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

  const radius = 4;
  const ex = cx + radius * Math.cos(t);
  const ey = cy + radius * Math.sin(t);

  const brightness = (8 - dist(x, y, ex, ey)) / 8;

  const r = lerp(0, 255, (1 + Math.cos(0.3 * t)) / 2 * brightness);
  const g = 0;
  const b = lerp(0, 255, (1 + Math.cos(0.3 * t + Math.PI)) / 2 * brightness);
  const a = lerp(0, 255, (1 - brightness) * 0.3);

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

  nodes.push([1, 1]);
  nodes.push([3, 8]);
  nodes.push([7, 2]);
  nodes.push([9, 9]);

  /*for (let i = 0; i < 4; i++) {
    nodes.push([Math.random() * 11, Math.random() * 11]);
  }*/

  const canvas = document.createElement('canvas');
  canvas.width = 11;
  canvas.height = 11;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, 11, 11);
  //ctx.lineWidth = 0.8;
  ctx.strokeStyle = '#fff';

  function line(n1, n2) {
    ctx.moveTo(n1[0], n1[1]);
    ctx.lineTo(n2[0], n2[1]);
    ctx.stroke();
  }

  line(nodes[0], nodes[2]);
  line(nodes[2], nodes[1]);
  line(nodes[1], nodes[3]);

  /*nodes.forEach(n1 => nodes.forEach(n2 => {
    if (n1 !== n2) {
      line(n1, n2);
    }
  }));*/

  const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

  return (iteration, x, y) => {
    const [minDist, nearNodeIndex] = nodes.reduce(([d, nIdx], [nx, ny], i) => {
      const thisDist = dist(x, y, nx, ny);
      return thisDist < d ? [thisDist, i] : [d, nIdx];
    }, [Infinity, undefined]);

    const t = iteration / 10.0;
    const radius = 2.3 * (1 + Math.sin(t + nearNodeIndex * Math.PI / 2)) / 2;

    const i = (canvas.width * y + x) * 4;
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    const a = minDist < radius ? 255 : 0;

    return [r, g, b, a];
  };
})();

const shadeSpiral = (() => {
  const spiralIndex = [];

  for (let y = 0; y < 12; y++) {
    const row = [];
    for (let x = 0; x < 12; x++) {
      row.push(0);
    }
    spiralIndex.push(row);
  }

  let x = 5;
  let y = 5;
  let i = 0;
  let sideLen = 1;
  let sideCnt = sideLen;
  let dir = 0;

  while (x >= 0 && x < 12 && y >= 0 && y < 12) {
    spiralIndex[y][x] = i;
    i += 1;

    switch (dir) {
      case 0:
        y -= 1;
        break;
      case 1:
        x -= 1;
        break;
      case 2:
        y += 1;
        break;
      case 3:
        x += 1;
        break;
    }

    sideCnt -= 1

    if (sideCnt <= 0) {
      dir += 1;
      dir %= 4;

      if (dir % 2 == 0) {
        sideLen += 1;
      }

      sideCnt = sideLen;
    }
  }

  return (t, x, y) => {
    const r = 0;
    const g = 0;
    const b = 0;
    const a = (5 * t + lerp(0, 255, spiralIndex[y][x] / (11 * 11))) % 255;

    return [r, g, b, a];
  };
})();

let currentShader = shadePlasma;

let time = 0;
function render() {
  for (let y = 0; y < leds.height; y++) {
    for (let x = 0; x < leds.width; x++) {
      const [r, g, b, a] = currentShader(time, x, y);
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

const animations = {
  'Plasma': shadePlasma,
  'Breathing': shadeBreathing,
  'Rotating Circle': shadeRotatingCircle,
  'Mouse Position': shadeMousePosition,
  'Spiral': shadeSpiral,
  'Network': shadeNetwork,
};

const animationSelectEl = document.getElementById('animations');

for (let animationName in animations) {
  const optionEl = document.createElement('option');
  optionEl.setAttribute('value', animationName);
  optionEl.innerHTML = animationName;
  animationSelectEl.appendChild(optionEl);
}

animationSelectEl.onchange = () => {
  const animationName = animationSelectEl.value;
  console.log(`Switching to ${animationName}`);
  currentShader = animations[animationName];
};
