import math
import random
import time

import HAL
import WebGUI

MAP = WebGUI.getMap(
    "/resources/exercises/montecarlo_laser_loc/images/mapgrannyannie.png"
)

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

NUM_PARTICLES = 300

WORLD_X_MIN = -4.5
WORLD_X_MAX = 0.5

WORLD_Y_MIN = -0.5
WORLD_Y_MAX = 5.5

MOTION_STD_X = 0.02
MOTION_STD_Y = 0.02
MOTION_STD_TH = 0.03

LASER_SIGMA = 0.20


# ==========================================================
# PARTÍCULA
# ==========================================================

class Particle:

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.weight = 1.0 / NUM_PARTICLES

    def copy(self):
        p = Particle(self.x, self.y, self.theta)
        p.weight = self.weight
        return p


# ==========================================================
# FILTRO DE PARTÍCULAS
# ==========================================================

class ParticleFilter:

    def __init__(self):
        self.particles = []
        self.previous_odom = HAL.getOdom()
        self.initialize()

    def initialize(self):
        self.particles.clear()
        for _ in range(NUM_PARTICLES):
            x = random.uniform(WORLD_X_MIN, WORLD_X_MAX)
            y = random.uniform(WORLD_Y_MIN, WORLD_Y_MAX)
            theta = random.uniform(-math.pi, math.pi)
            self.particles.append(Particle(x, y, theta))
        print("Inicializadas", len(self.particles), "partículas")

    def world_to_pixel(self, x, y):
        px = int(101.1 * (4.2 + y))
        py = int(101.1 * (5.7 - x))
        return px, py

    def is_wall(self, px, py):
        if px < 0 or py < 0:
            return True
        if px >= MAP.shape[1] or py >= MAP.shape[0]:
            return True
        pixel = MAP[py, px]
        return pixel[0] < 0.5

    def ray_cast(self, x, y, theta):
        distance = 0.0
        step = 0.05
        while distance < 8.0:
            rx = x + distance * math.cos(theta)
            ry = y + distance * math.sin(theta)
            px, py = self.world_to_pixel(rx, ry)
            if self.is_wall(px, py):
                return distance
            distance += step
        return 8.0  

    def motion_update(self):
        odom = HAL.getOdom()
        dx = odom.x - self.previous_odom.x
        dy = odom.y - self.previous_odom.y
        dtheta = odom.yaw - self.previous_odom.yaw
        self.previous_odom = odom

        for p in self.particles:
            p.x += dx + random.gauss(0, MOTION_STD_X)
            p.y += dy + random.gauss(0, MOTION_STD_Y)
            p.theta += dtheta + random.gauss(0, MOTION_STD_TH)

            while p.theta > math.pi:
                p.theta -= 2 * math.pi
            while p.theta < -math.pi:
                p.theta += 2 * math.pi

    def observation_update(self):
        laser = HAL.getLaserData()
        total_weight = 0.0
        max_index = len(laser.values) - 1

        for p in self.particles:
            weight = 1.0

            for angle in [-90, -45, 0, 45, 90]:
                index = angle + 90
                index = max(0, min(index, max_index))
                
                real = laser.values[index]
                
                if math.isinf(real) or math.isnan(real):
                    real = 8.0

                simulated = self.ray_cast(
                    p.x,
                    p.y,
                    p.theta + math.radians(angle)
                )

                error = real - simulated

                weight *= math.exp(
                    -(error ** 2) /
                    (2 * (LASER_SIGMA ** 2))
                )

            p.weight = weight
            total_weight += weight

        # CORREÇÃO DA NORMALIZAÇÃO DOS PESOS (BLINDADA CONTRA ZEROS)
        if total_weight > 0:
            for p in self.particles:
                p.weight /= total_weight
        else:
            for p in self.particles:
                p.weight = 1.0 / NUM_PARTICLES

    def resample(self):
        new_particles = []
        cumulative = []
        total = 0.0

        for p in self.particles:
            total += p.weight
            cumulative.append(total)

        for _ in range(NUM_PARTICLES):
            r = random.uniform(0, total)
            for i, c in enumerate(cumulative):
                if r <= c:
                    new_particles.append(self.particles[i].copy())
                    break

        self.particles = new_particles
        for p in self.particles:
            p.weight = 1.0 / NUM_PARTICLES

    def estimate_pose(self):
        x = 0.0
        y = 0.0
        sin_sum = 0.0
        cos_sum = 0.0

        for p in self.particles:
            x += p.x * p.weight
            y += p.y * p.weight
            sin_sum += math.sin(p.theta) * p.weight
            cos_sum += math.cos(p.theta) * p.weight

        theta = math.atan2(sin_sum, cos_sum)
        return x, y, theta

    def publish_particles(self):
        data = []
        for p in self.particles:
            data.append([p.x, p.y, p.theta])
        WebGUI.showParticles(data)


# ==========================================================
# LOOP PRINCIPAL - ALGORITMO COMPLETO COMPACTADO
# ==========================================================

pf = ParticleFilter()
print("Filtro MCL Inicializado e Pronto para Validação!")

contador = 0

while True:
    pf.motion_update()
    pf.observation_update()  
    
    # Estimando a pose com os pesos atualizados do laser (antes do resample)
    x, y, theta = pf.estimate_pose()
    
    # Print limpo no terminal (aproximadamente 1 vez por segundo)
    if contador % 20 == 0:
        print(f"Pose Estimada -> X: {x:.2f}, Y: {y:.2f}, Theta: {math.degrees(theta):.1f}°")
    
    contador += 1

    pf.resample()             
    pf.publish_particles()
    time.sleep(0.05)
