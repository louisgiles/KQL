# Correlated context timeline

`correlated-context.kql` creates a short, source-labelled timeline after an
incident has already been scoped to at least one actor, device, or IP.

## Inputs

- `TargetUPN`, `TargetDeviceId`, `TargetDeviceName`, and `TargetIP`: supply at
  least one; combine them only when they are already known to belong together.
- `AnchorTime`: incident reference time.
- `Lookback` and `Lookforward`: default to two hours and one hour.
- `MaxRows`: defaults to 30.

## Dependencies

At least one referenced table must exist. Identity, Azure, Microsoft 365, and
Defender endpoint tables are optional relative to each other. A missing domain
is a coverage limitation, not benign evidence.

## Output and decision

The query normalizes identity, Azure control-plane, Microsoft 365, process,
file, and network events to the shared investigation schema. It sorts a maximum
of 30 evidence rows chronologically and adds explicit invalid-input, no-data,
or truncation status rows.

Use it to answer whether observed activity forms a coherent cross-domain
sequence and whether containment should include more users, devices, sessions,
or cloud resources. It does not calculate a maliciousness score.

## Validation limits

Parser validation is schema-blind. Validate source-column availability and
runtime behavior in each target tenant before relying on the timeline during
an incident.
