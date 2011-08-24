Server Reliability Notes
========================

Back-end
~~~~~~~~
- With multiple servers, they can be taken out of action one at a time, upgrades
  done, and put back into service; that way, the service as a whole is always up
  - Alterations to the database schema require all database servers to be updated
    at once
- With multiple servers, errors can be automatically detected and a crashed server
  can be routed around

Front-end
~~~~~~~~~
- If a server is rebooted in a controlled way, uploads in progress can be allowed
  to finish; if it crashes, they will need restarting
  - Article text is saved as drafts, so a lost connection won't lose everything
