# tkvalidate
Validation functions that only allow integers or floats for tkinter `Entry` widgets

The validate functions are called with an `Entry` widget as an argument. The following code will validate an `Entry` so 
only integers in the range -5 to 5 may be entered. 

    import tkinter as tk

    root = tk.Tk()
    widget = tk.Entry(root, justify=tk.CENTER)
    widget.pack(padx=10, pady=10)
    int_validate(widget, from_=-5, to=5)
    root.mainloop()

This works on any subclass of `Entry`. For a `ttk.Spinbox` it can take the limits directly from the `Spinbox`. The 
following code accomplishes the same as the previous but with a `Spinbox`.

    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    widget = ttk.Spinbox(root, justify=tk.CENTER, from_=-5, to=5)
    widget.pack(padx=10, pady=10)
    int_validate(widget)
    root.mainloop()

For validating floating points instead of integers, simply use `float_validate` instead.