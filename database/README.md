# Database

This directory holds the SQLite schema and (at runtime) the live database file.

| File | Description |
|------|-------------|
| `schema.sql` | CREATE TABLE statements for all platform tables |
| `minimal_plc.db` | Live database (created at runtime, excluded from git) |

## Tables

| Table | Description |
|-------|-------------|
| `projects` | Saved HMI screens and PLC programs |
| `bacnet_devices` | Discovered BACnet/IP devices |
| `bacnet_points` | BACnet object points with alarm thresholds |
| `point_history` | Time-series value log |
| `alarms` | Alarm events |
| `users` | Platform users |
| `network_config` | Key-value configuration store |
| `audit_log` | User action audit trail |
