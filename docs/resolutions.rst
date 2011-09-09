Multi-resolution Support
~~~~~~~~~~~~~~~~~~~~~~~~

We should support:

* 480px  (mobile):     thin mode
* 640px  (mobile):     thin mode
* 800px  (obsolete):   thin mode (it's a PC res, but we don't want to support it in full mode)
* 960px  (Half HD):    normal mode + header tweak
* 1024px (PC):         normal mode + header tweak
* 1200px (PC):         normal mode


To do this we have:

  @media(max-width: 900px) {
      override some styles for thin mode
  }

