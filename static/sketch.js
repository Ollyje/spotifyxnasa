let planets = [];
let sun;

function setup() {
  createCanvas(1920, 1080, WEBGL); // Set the renderer to WEBGL for 3D
  sun = new Planet(0, 0, 0, 60); // Sun in the center (not moving)
  for (let i = 0; i < 30; i++) {
    let radius = random(100, 500); // Random orbit radius for each planet
    let size = random(5, 15);      // Random size for each planet
    let speed = random(0.01, 0.05); // Random speed for each planet
    planets.push(new PlanetOrbit(sun, radius, size, speed));
  }
}

function draw() {
  background(0); // Black background
  rotateY(frameCount * 0.002); // Slow rotation to see orbits better

  // Draw the sun and the planets
  sun.show();
  for (let planet of planets) {
    planet.update();
    planet.showTrail();
    planet.show();
  }

  // Draw lines connecting each planet (optional)
  stroke(200, 100); // Light gray lines with slight transparency
  for (let i = 0; i < planets.length; i++) {
    for (let j = i + 1; j < planets.length; j++) {
      let p1 = planets[i].getPosition();
      let p2 = planets[j].getPosition();
      line(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z);
    }
  }
}

class Planet {
  constructor(x, y, z, size) {
    this.position = createVector(x, y, z);
    this.size = size;
  }

  show() {
    push();
    translate(this.position.x, this.position.y, this.position.z);
    fill(200); // Light gray for the sun
    noStroke();
    sphere(this.size); // Display as a 3D sphere
    pop();
  }
}

class PlanetOrbit {
  constructor(center, orbitRadius, size, speed) {
    this.center = center;
    this.orbitRadius = orbitRadius;
    this.size = size;
    this.angle = random(TWO_PI);    // Start at a random angle
    this.orbitTilt = random(-PI/6, PI/6); // Random tilt angle for 3D effect
    this.speed = speed;
    this.trail = [];                // To store trail positions
  }

  update() {
    this.angle += this.speed;

    // Calculate 3D position
    let x = this.center.position.x + cos(this.angle) * this.orbitRadius * cos(this.orbitTilt);
    let y = this.center.position.y + sin(this.angle) * this.orbitRadius * sin(this.orbitTilt);
    let z = this.center.position.z + sin(this.angle) * this.orbitRadius * cos(this.orbitTilt);

    // Add current position to trail
    this.trail.push(createVector(x, y, z));
    if (this.trail.length > 20) { // Limit trail length
      this.trail.shift();
    }
  }

  getPosition() {
    let x = this.center.position.x + cos(this.angle) * this.orbitRadius * cos(this.orbitTilt);
    let y = this.center.position.y + sin(this.angle) * this.orbitRadius * sin(this.orbitTilt);
    let z = this.center.position.z + sin(this.angle) * this.orbitRadius * cos(this.orbitTilt);
    return createVector(x, y, z);
  }

  showTrail() {
    noFill();
    stroke(150); // Darker gray for trail
    strokeWeight(1);

    beginShape();
    for (let pos of this.trail) {
      vertex(pos.x, pos.y, pos.z);
    }
    endShape();
  }

  show() {
    let pos = this.getPosition();
    push();
    translate(pos.x, pos.y, pos.z);
    fill(255); // White for planets
    noStroke();
    sphere(this.size); // Display as a 3D sphere
    pop();
  }
}