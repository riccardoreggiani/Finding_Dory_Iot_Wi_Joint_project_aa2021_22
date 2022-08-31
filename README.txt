--- FINDING DORY ---
--- Andrea Prisciantelli & Riccardo Reggiani ---

--- README ---

Inside this .zip folder you can find:

- parser.py, which is the Python script code used to parse the given input fingerprint dataset, compute the RSSIs measurements at odd position and Dory's location
- input.txt, containing the fingerprint dataset with ONLY even positions (found with MQTT and CoAP)
- output.txt, containing BOTH odd and even position (computed by the Python code)
- report file, explaining project development steps, the algorithm and assumptions

--- NOTE ABOUT PYTHON SCRIPT ---
Inside the Python script (parser.py) some lines of code are commented. They have been used for debug purposes (e.g. printing positions, RSSIs and so on).
These lines of code can be useful in order to better understand the steps of this code and so they have not been removed.
Even if they are not necessary for this script to run properly, you can still remove the '#' and you'll see some output in the Shell terminal.

Dory's location is printed in the terminal and is also available in the report file.