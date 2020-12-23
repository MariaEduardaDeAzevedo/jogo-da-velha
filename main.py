import tkinter as tk

window = tk.Tk()
window.geometry("368x200")
window["bg"] = "black"

title = tk.Label(text="JOGO DA VELHA", font="Ubuntu 32", fg="white", bg="black")
title.grid(row=0, column=1)

nickname_label = tk.Label(text="DIGITE SEU NOME", font="Ubuntu 16", fg="white", bg="black")
nickname_label.grid(row=1, column=1)

nickname = tk.Entry(width=30, font="Ubuntu 16")
nickname.grid(row=2, column=1)

x_button = tk.Button(text="X", font="Ubuntu 32", fg="white", bg="black")
x_button.grid(row=3, column=1, sticky="W")

o_button = tk.Button(text="O", font="Ubuntu 32", fg="white", bg="black")
o_button.grid(row=3, column=1, sticky="E")

start_button = tk.Button(text="JOGAR", font="Ubuntu 32", fg="white", bg="black")
start_button.grid(row=3, column=1, sticky="N")
window.mainloop()