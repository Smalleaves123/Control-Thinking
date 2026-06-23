# Future Improvements

## 1. Short-Term Improvements

- Add automatic checks for collinearity.
- Add condition-number monitoring for B1 and B4.
- Add random seed control for reproducible simulations.
- Add unit tests for signed angle computation.
- Add unit tests for rotation matrix conventions.
- Add visualization of triangle shape changes over time.

## 2. Medium-Term Extensions

- Implement the unaligned three-follower case.
- Add noisy measurement simulations.
- Compare linear localization and robust localization.
- Test different motion patterns.
- Analyze the influence of sampling interval.
- Add more agents and mixed follower-landmark-leader topologies.

## 3. Long-Term Research Ideas

- Combine relative localization with formation control.
- Use active motion planning to avoid ill-conditioned configurations.
- Extend the simulation to 3D if the theory is adapted.
- Integrate bearing and distance measurements in addition to signed angles.
- Study how communication constraints affect distributed relative localization.
- Connect this work with angle rigidity and multi-agent formation stabilization.

## 4. Possible Follow-Up Papers

This paper naturally connects to:

- angle rigidity,
- bearing rigidity,
- formation control,
- SLAM observability,
- sensor array calibration,
- communication-constrained coordinated control.

A good next paper is Angle Rigidity and Its Usage to Stabilize Multiagent Formations in 2-D, because it also relies on local angle measurements and does not require globally aligned coordinate frames.
