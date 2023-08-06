Launch
======


There are 3 ways to launch **tridesclous**:
  * Inside a **jupyter notebook**: this is the best
  * With a Graphical User Interface (GUI): the least frightening for beginners
  * With command line in a bash terminal: for 90s nostalgic

  
Please read carrefully, the how and the why for each methods.


Method 1: Launching tridesclous inside a jupyter notebook
----------------------------------------------------------

This is the best method that authors recommend for users.
People that never code with python or any language can be scared about this but this is easy!

Keep in mind that for reproducible science you need to keep track of what you are doing and this is the best way.

Also note that magic all-in-one command line and GUI keep you away from deep understanding of your spike sorting tool chain.
Writting simple code block can help you a lot to realize and overcome difficulties.



So for this method:
  1. Launch jupyter notebook (easy if you have anaconda)
  2. Copy/paste this `notebook <https://github.com/tridesclous/tridesclous/blob/master/example/example_locust_dataset.ipynb>`_
  3. Read it carrefully.
  4. Modify it and do your spike sorting.



Method 2: Launching tridesclous GUI
------------------------------------

Here's the method for lazy people (or people in a hurry).

For demagogical reasons, we wrote a small GUI in Qt for launching tridesclous.



Do:
  * open a terminal::
  
      workon tdc  (or source activate tdc for windows)
      tdc
  
  * In the GUI you must:
      1. File>Initialize example_locust_dataset
      2. Select a channel group in **chan_grp**
      3. **Initialize catalogue**
      4. **Open catalogue Window**
      5. save catalogue when happy
      6. **run Peeler**
      7. **open PeelerWindow**

See :ref:`step_by_step` for complete explanation.


Method 3: launching tridesclous in a bash
------------------------------------------

Some other spike sorting projects propose a command line interface
for interacting with datasets and the spike sorting process.

Even if we are generally fan of the command line, in the context of spike
sorting we don't think it is smart way for launching.
There are so many parameters that all of them must be written in 
file. So writting all that parameters in a python script sound better.


Nevertheless, tridesclous has a command line interface to

  * intialize dataset::

      tdc init

  * Initialize catalogue constructor::
  
      tdc makecatalogue -d dirname -c chan_grp -p parameter_file.json
     
  * open catalogue window::
  
      tdc cataloguewin -d dirname -c chan_grp

  * Run peeler::
  
      tdc runpeeler -d dirname -c chan_grp
    
  * Open peeler window::
  
      tdc peelerwin -d dirname -c chan_grp








