# tap-hubplanner

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [Hub Planner](https://github.com/hubplanner/API)
- Extracts the following resources:
  - [Billing Rates](https://github.com/hubplanner/API/blob/master/Sections/billingrate.md)
  - [Project Bookings](https://github.com/hubplanner/API/blob/master/Sections/bookings.md)
  - [Clients](https://github.com/hubplanner/API/blob/master/Sections/clients.md)
  - [Events](https://github.com/hubplanner/API/blob/master/Sections/events.md)
  - [Project Groups](https://github.com/hubplanner/API/blob/master/Sections/groups.md)
  - [Resource Groups](https://github.com/hubplanner/API/blob/master/Sections/groups.md)
  - [Holidays](https://github.com/hubplanner/API/blob/master/Sections/holidays.md)
  - [Projects](https://github.com/hubplanner/API/blob/master/Sections/project.md)
  - [Resources](https://github.com/hubplanner/API/blob/master/Sections/resource.md)
  - [Unassigned Work](https://github.com/hubplanner/API/blob/master/Sections/unassigned-work.md)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Configuration

This tap requires a `config.json` which specifies details regarding authentication and other options. **`api_key` are required**

Config properties:

| Property | Required | Example | Description |
| -------- | -------- | ------- | ----------- |
| `api_key` | Y | "ac0ad1..." | A Hub Planner API key with Read Scope. |
| `start_date` | N | "2010-01-01T00:00:00Z" | The start date to use for date created or updated replication, when available.  |
| `user_agent` | N | "Vandelay Industries ETL Runner (+contact@example.org)" | The user agent to send on every request. |

## Usage

1. Install
  ```bash
  pip install tap-hubplanner
  ```

2. Create the config file

  Create a JSON file called `config.json`. Its contents should look like:

  ```json
  {
      "api_key": "<Hub Planner API Key>",
      "start_date": "2000-01-01T00:00:00Z",
      "user_agent": "Acme (+acme@example.com)"
  }
  ```

  The `api_key` is the API key for your Hub Planner account with Read Scope.

  The `start_date` specifies the date at which the tap will begin pulling data.

  The `user_agent` parameter provide a User-Agent strings denoting your application.

4. Run the Tap in Discovery Mode

    ```bash
    tap-hubplanner --config config.json --discover > catalog.json
    ```

   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).

5. Run the Tap in Sync Mode

    ```bash
    tap-hubplanner --config config.json --catalog catalog.json
    ```

---

Copyright &copy; 2019 Rangle.io
