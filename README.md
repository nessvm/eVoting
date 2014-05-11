Computer-based electronic voting system (eVoting)
================================================

Three entities are defined:

1. **Caster(CST)**
Client side of the system only, caster emits its vote, which is blinded with a random number coprime with the n of the public keys, sends the blinded vote to the Validator, and the random number generated to the Counter.

2. **Validator(VTR)**
First

3. **Counter(CTR)**

System Frame Header Format (bytes):

[0-7] - Operation Code
[8-72] - Vote identifier
[72-4024] - Ciphered Data
