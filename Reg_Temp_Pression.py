import multiprocessing
import random
import time
import curses

# Shared memory for temperature and pressure
manager = multiprocessing.Manager()

#Initial conditions
memT = manager.Value('d', 23.0)
memP = manager.Value('d', 100000.0)
go_chauffage = manager.Value('b', False)
go_pompe = manager.Value('b', False)

# Lock for shared memory
mem_lock = manager.Lock()

# Constants
SEUIL_T = 25.0
SEUIL_P = 101000.0




# Temperature and pressure sensors
def lire_capteur(memT, memP):
    while True:
        time.sleep(1)
        x = random.randint(0, 1)
        alpha = 0.1 if x == 0 else -0.1
        with mem_lock:
            memT.value += alpha
            memP.value += alpha

# Controller process
def controller(memT, memP, go_pompe, go_chauffage):

    while True:
        time.sleep(1)

        with mem_lock:
            T = memT.value
            P = memP.value
        
        if T > SEUIL_T:
            go_chauffage.value = False

            if P > SEUIL_P:
                go_pompe.value = True
            else:
                go_pompe.value = False

        elif T < SEUIL_T:

                go_pompe.value = True
                go_chauffage.value = True
        else:
            go_chauffage.value = False

            if(P >SEUIL_P):
                go_pompe.value = True
            else:
                go_pompe.value = False   


# Heater process
def chauffage(memT, go_chauffage):
    while True:
        time.sleep(3)
        if go_chauffage.value:
            with mem_lock:
                memT.value += random.uniform(0.25, 0.5)

# Pressure pump process
def pompe(memP, go_pompe):
    while True:
        time.sleep(3)
        if go_pompe.value:
            with mem_lock:
                memP.value += random.uniform(20, 50)

# # Screen display process
# def ecran(memT, memP):
#     while True:
#         time.sleep(1)
#         with mem_lock:
#             T = memT.value
#             P = memP.value

#         print(f"Temperature: {T:.2f} Pression: {P:.2f}")
#         print("Chauffage: ",go_chauffage.value, "Pompe: ", go_pompe.value)

def ecran(mem_T, mem_P, go_chauffage, go_pompe):

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        while True:
            stdscr.clear()
            stdscr.addstr("Température : {:.2f}\n".format(mem_T.value))
            stdscr.addstr("Pression : {:.2f}\n".format(mem_P.value))
            stdscr.addstr("Chauffage : {}\n".format("ON" if go_chauffage.value else "OFF"))
            stdscr.addstr("Pompe : {}\n".format("ON" if go_pompe.value else "OFF"))
            stdscr.refresh()
            time.sleep(1)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()


if __name__ == '__main__':
    # Start all processes
    capteur_process = multiprocessing.Process(target=lire_capteur, args=(memT, memP))
    capteur_process.start()

    controller_process = multiprocessing.Process(target=controller, args=(memT, memP, go_pompe, go_chauffage))
    controller_process.start()

    chauffage_process = multiprocessing.Process(target=chauffage, args=(memT, go_chauffage))
    chauffage_process.start()

    pompe_process = multiprocessing.Process(target=pompe, args=(memP, go_pompe))
    pompe_process.start()

    ecran_process = multiprocessing.Process(target=ecran, args=(memT, memP, go_pompe, go_chauffage))
    ecran_process.start()

    # Wait for all processes to finish
    capteur_process.join()
    controller_process.join()
    chauffage_process.join()
    pompe_process.join()
    ecran_process.join()
