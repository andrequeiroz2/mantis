INSERT INTO type_devices(name)
VALUES('Sensor'), ('Actuator');

INSERT INTO qos(qos) VALUES (0), (1), (2);

--INSERT INTO icons(name, icon, type_device) VALUES
--('hub', 'FaHubspot', 'hub'),
--('thermometer', 'BsThermometerHigh', 'sensor'),
--('humidity', 'WiHumidity', 'sensor'),
--('valve', 'GiValve', 'actuator'),
--('lamp', 'GiDeskLamp', 'actuator'),
--('power', 'ImPower', 'actuator'),
--('electrical outlet', 'ImPowerCord', 'actuator'),
--('engine', 'TbEngine', 'actuator');

INSERT INTO type_sensors(name, max_scale, min_scale, icons_id)
VALUES
('DHT11-Temperature', 50, 0, 1),
('DHT11-Humidity', 80, 20, 2),
('DHT22-Temperature', 80, -40, 1),
('DHT22-Humidity', 100, 0,  2),
('lm39x-Solo Humidity', 100, 0, 3);

INSERT INTO measures(name, scale, icon_id)
VALUES
("Temperature", 'C', 1),
("Humidity", '%', 2),
("Soil Humidity", '%', 3)

INSERT INTO icon_sensors (font)
VALUES
("faTemperatureFull"),
("faDroplet")
("faHandHoldingDroplet")

--INSERT INTO type_actuators(name, icons_id)
--VALUES
--('Relay', 6),
--('Valve', 4),
--('Lamp', 5),
--('Engine', 8),
--('Electrical-Outlet', 7);