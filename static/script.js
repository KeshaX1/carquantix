// Dataset: update image paths or replace with placeholders
const VEHICLES = [
  { id: 'R8',              name: '2024 Audi R8',       power:570, acc:3.2, topSpeed:330, engine: '5.2 V10', price: '$239.800', img: '/static/images/audiR8.jpg', rearImg: '/static/rearimg/audiR8-rear.jpg', consumption: { value: 14.8, unit: 'L/100km' }},

  { id: 'A1',              name: '2024 Audi A1',       power:110, acc:10.5, topSpeed:194, engine: '30 TFSI', price: '$22.490', img: '/static/images/audiA1.png', rearImg: '/static/rearimg/audiA1-rear.png', consumption: { value: 5.4, unit: 'L/100km' }},

  { id: 'A2',              name: '2001 Audi A2',       power:173, acc:12.3, topSpeed:173, engine: '1.4i 16V', price: '$3.990', img: '/static/images/audiA2.png', rearImg: '/static/rearimg/audiA2-rear.png', consumption: { value: 6.5, unit: 'L/100km' }},

  { id: 'A3',              name: '2024 Audi A3',       power:204, acc:6.3, topSpeed:250, engine: '40 TFSI', price: '$29.470', img: '/static/images/audiA3.png', rearImg: '/static/rearimg/audiA3-rear.png', consumption: { value: 6.3, unit: 'L/100km' }},

  { id: 'A4',              name: '2023 Audi A4',       power:204, acc:6.7, topSpeed:210, engine: '40 TFSI', price: '$29.499', img: '/static/images/audiA4.jpg', rearImg: '/static/rearimg/audiA4-rear.png', consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'A5',              name: '2023 Audi A5',       power:268, acc:5.9, topSpeed:210, engine: '45 TFSI', price: '$40.980', img: '/static/images/audiA5.jpg', rearImg: '/static/rearimg/audiA5-rear.png', consumption: { value: 7.6, unit: 'L/100km' }},

  { id: 'A6',              name: '2022 Audi A6',       power:340, acc:5.1, topSpeed:250, engine: '55 TFSI', price: '$49.950', img: '/static/images/audiA6.jpg', rearImg: '/static/rearimg/audiA6-rear.png', consumption: { value: 8.8, unit: 'L/100km' }},

  { id: 'A7',              name: '2022 Audi A7',       power:340, acc:5.0, topSpeed:250, engine: '55 TFSI V6', price: '$45.000', img: '/static/images/audiA7.png', rearImg: '/static/rearimg/audiA7-rear.png', consumption: { value:9.4, unit: 'L/100km' }},

  { id: 'SQ2',             name: '2022 Audi SQ2',       power:300, acc:4.9, topSpeed:250, engine: '2.0 TFSI', price: '$28.950', img: '/static/images/audiSQ2.png', rearImg: '/static/rearimg/audiSQ2-rear.png', consumption: { value: 7.3, unit: 'L/100km' }},

  { id: 'SQ5',             name: '2022 Audi SQ5',       power:341, acc:5.1, topSpeed:250, engine: '3.0 TDI V6', price: '$48.879', img: '/static/images/audiSQ5.png', rearImg: '/static/rearimg/audiSQ5-rear.png', consumption: { value:8.3, unit: 'L/100km' }},

  { id: 'Q5',              name: '2024 Audi Q5',        power:261, acc:6.1, topSpeed:240, engine: '45 TFSI quattro', price: '$45.400', img: '/static/images/audiSQ5.png', rearImg: '/static/rearimg/audiSQ5-rear.png', consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'SQ6 e-tron',      name: '2024 Audi SQ6 e-tron', power:489, acc:4.4, topSpeed:230, engine: '100 kWh', price: '$77.900', img: '/static/images/audiSQ6 e-tron.png', rearImg: '/static/rearimg/audiSQ6 e-tron-rear.png', consumption: { value:21.0, unit: 'kWh/100km' }},

  { id: 'SQ7',             name: '2024 Audi SQ7',       power:507, acc:4.1, topSpeed:250, engine: '4.0 TFSI V8 ', price: '$110.490', img: '/static/images/audiSQ7.png', rearImg: '/static/rearimg/audiSQ7-rear.png', consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'Q7',              name: '2024 Audi Q7',        power:335, acc:5.8, topSpeed:250, engine: '55 TFSI quattro', price: '$61.795', img: '/static/images/audiSQ7.png', rearImg: '/static/rearimg/audiSQ7-rear.png', consumption: { value:9.5, unit: 'L/100km' }},

  { id: 'SQ8',             name: '2025 Audi SQ8',       power:507, acc:4.1, topSpeed:250, engine: '4.0 TFSI V8', price: '$107.900', img: '/static/images/audiSQ8.png', rearImg: '/static/rearimg/audiSQ8-rear.png', consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'Q8',              name: '2024 Audi Q8',        power:335, acc:5.9, topSpeed:250, engine: '55 TFSI quattro', price: '$73.700', img: '/static/images/audiSQ8.png', rearImg: '/static/rearimg/audiSQ8-rear.png', consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'SQ8 e-tron',      name: '2023 Audi SQ8 e-tron',  power:503, acc:4.5, topSpeed:210, engine: '114 kWh', price: '$67.774', img: '/static/images/audiSQ8 e-tron.jpg', rearImg: '/static/rearimg/audiSQ8 e-tron-rear.png', consumption: { value:25.0, unit: 'kWh/100km' }},

  { id: 'e-tron',          name: '2024 Audi e-tron',    power:402, acc:5.6, topSpeed:200, engine: '95 kWh', price: '$66.800', img: '/static/images/audiSQ8 e-tron.jpg', rearImg: '/static/rearimg/audiSQ8 e-tron-rear.png', consumption: { value:22.0, unit: 'kWh/100km' }},

  { id: 'e-tron GT',       name: '2024 Audi RS e-tron GT',  power:680, acc:3.3, topSpeed:250, engine: '93.4 kWh (Electric)', price: '$119.800', img: '/static/images/audie-tron GT.jpg', rearImg: '/static/rearimg/audie-tron GT-rear.png', consumption: { value: 21.5, unit: 'kWh/100km' }},

  { id: 'RS Q3',           name: '2024 Audi RS Q3',    power:400, acc:4.5, topSpeed:250, engine: '2.5L TFSI Inline-5 Turbo', price: '$65.950', img: '/static/images/audiRSQ3.jpg', rearImg: '/static/rearimg/audiRSQ3-rear.png', consumption: { value: 10.4, unit: 'L/100km' }},

  { id: 'RS Q5',           name: '2021 Audi RS Q5',    power:299, acc:4.3, topSpeed:280, engine: '50 TFSIe S-Line', price: '$48.500', img: '/static/images/audiRSQ5.jpg', rearImg: '/static/rearimg/audiRSQ5-rear.png', consumption: { value: 9.3, unit: 'L/100km' }},

  { id: 'RS Q8',           name: '2025 Audi RS Q8',    power:640, acc:3.6, topSpeed:250, engine: '4.0 TFSI quattro performance', price: '$155.970', img: '/static/images/audiRSQ8.jpg', rearImg: '/static/rearimg/audiRSQ8-rear.png', consumption: { value: 13.8, unit: 'L/100km' }},

  { id: 'RS2',             name: '1995 Audi RS2',      power:315, acc:5.4, topSpeed:262, engine: '2.2 turbo 20V cat Avant quattro', price: '$69.000', img: '/static/images/audiRS2.jpg', rearImg: '/static/rearimg/audiRS2-rear.png' , consumption: { value:14.5, unit: 'L/100km' }},

  { id: 'RS3',             name: '2024 Audi RS3',      power:400, acc:3.8, topSpeed:250, engine: '2.5 TFSI quattro S tronic', price: '$67.930', img: '/static/images/audiRS3.jpg', rearImg: '/static/rearimg/audiRS3-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'RS4',             name: '2024 Audi RS4',      power:450, acc:3.7, topSpeed:300, engine: '2.9 TFSI 450CV quattro Tipt', price: '$96.500', img: '/static/images/audiRS4.jpg', rearImg: '/static/rearimg/audiRS4-rear.jpg' , consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'RS5',             name: '2024 Audi RS5',      power:470, acc:3.7, topSpeed:300, engine: '2.9 tfsi quattro 450cv tiptronic', price: '$87.900', img: '/static/images/audiRS5.jpg', rearImg: '/static/rearimg/audiRS5-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'RS6',             name: '2024 Audi RS6',      power:630, acc:3.3, topSpeed:305, engine: 'GT 4.0 TFSI V8', price: '$132.980', img: '/static/images/audiRS6.jpg', rearImg: '/static/rearimg/audiRS6-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'RS7',             name: '2024 Audi RS7',      power:630, acc:3.4, topSpeed:280, engine: 'performance 4.0 TFSI V8', price: '$155.400', img: '/static/images/audiRS7.jpg', rearImg: '/static/rearimg/audiRS7-rear.jpg' , consumption: { value:13.5, unit: 'L/100km' }},
  
  { id: 'TT RS',           name: '2024 Audi TT RS',    power:400 , acc:3.9, topSpeed:250, engine: '2.5 TFSI quattro S tronic', price: '$84.980', img: '/static/images/audiTTRS.jpg', rearImg: '/static/rearimg/audiTTRS-rear.jpg' , consumption: { value:9.5, unit: 'L/100km' }},

  { id: 'TTS',             name: '2023 Audi TTS',      power:320, acc:4.5, topSpeed:250, engine: '2.0 TFSI quattro S tronic', price: '$61.500', img: '/static/images/audiTTRS.jpg', rearImg: '/static/rearimg/audiTTRS-rear.jpg' , consumption: { value:8.2, unit: 'L/100km' }},

  { id: 'A8',              name: '2024 Audi A8',       power:460, acc:4.8, topSpeed:250, engine: '60 TFSI V8', price: '$79.620', img: '/static/images/audiA8.jpg', rearImg: '/static/rearimg/audiA8-rear.png' , consumption: { value:9.8, unit: 'L/100km' }},

  { id: '118',             name: '2023 BMW 118',        power:150, acc:8.4, topSpeed:216, engine: '118d', price: '$21.990', img: '/static/images/bmw118.png', rearImg: '/static/rearimg/bmw118-rear.png' , consumption: { value:4.1, unit: 'L/100km' }},

  { id: '120',             name: '2024 BMW 120',        power:170, acc:7.8, topSpeed:226, engine: '120 Mild Hybrid Steptronic DCT', price: '$29.990', img: '/static/images/bmw120.png', rearImg: '/static/rearimg/bmw120-rear.png' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: '140',             name: '2019 BMW 140',        power:340, acc:4.4, topSpeed:250, engine: 'M140i', price: '$33.500', img: '/static/images/bmw140.jpg', rearImg: '/static/rearimg/bmw140-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: '218',             name: '2024 BMW 218',        power:136, acc:9.1, topSpeed:215, engine: '218i', price: '$26.900', img: '/static/images/bmw218.png', rearImg: '/static/rearimg/bmw218-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: '220',             name: '2020 BMW 220',       power:190, acc:7.1, topSpeed:230, engine: '220d', price: '$22,400', img: '/static/images/bmw220.jpg', rearImg: '/static/rearimg/bmw220-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id:'223',              name: '2025 BMW 223',       power:218, acc:6.4, topSpeed:250, engine: '223 Mild Hybrid xDrive Steptronic DCT', price: '$40,990', img: '/static/images/bmw223.png', rearImg: '/static/rearimg/bmw223-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id:'225',              name: '2022 BMW 225',       power:224, acc:6.7, topSpeed:202, engine: '225xe', price: '$28,900', img: '/static/images/bmw225.png', rearImg: '/static/rearimg/bmw225-rear.png' , consumption: { value:6.7, unit: 'L/100km' }},

  { id:'228',              name: '2016 BMW 228',       power:245, acc:6.0, topSpeed:250, engine: '228i', price: '$21,500', img: '/static/images/bmw228.jpg', rearImg: '/static/rearimg/bmw228-rear.png' , consumption: { value:6.6, unit: 'L/100km' }},

  { id:'235',              name: '2024 BMW 235',       power:306, acc:4.8, topSpeed:250, engine: 'M235i', price: '$38,990', img: '/static/images/bmw235.png', rearImg: '/static/rearimg/bmw235-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id:'320',              name: '2024 BMW 320',       power:156, acc:9.1, topSpeed:222, engine: '320Li Steptronic', price: '$50,600', img: '/static/images/bmw320.png', rearImg: '/static/rearimg/bmw320-rear.png' , consumption: { value:7.5, unit: 'L/100km' }},

  { id:'418',              name: '2017 BMW 418',       power:136, acc:9.0, topSpeed:212, engine: '418i', price: '$17.499', img: '/static/images/bmw418.png', rearImg: '/static/rearimg/bmw418-rear.png' , consumption: { value:7.5, unit: 'L/100km' }},

  { id:'420',              name: '2025 BMW 420',       power:190, acc:7.6, topSpeed:233, engine: '420d Mild Hybrid xDrive Steptronic', price: '$53.399', img: '/static/images/bmw420.png', rearImg: '/static/rearimg/bmw420-rear.jpg' , consumption: { value:6.0, unit: 'L/100km' }},

  { id:'435',              name: '2016 BMW 435',       power:306, acc:5.2, topSpeed:250, engine: '435i', price: '$27.900', img: '/static/images/bmw435.png', rearImg: '/static/rearimg/bmw435-rear.jpg' , consumption: { value:9.5, unit: 'L/100km' }},

  { id:'525',              name: '2015 BMW 525',       power:218, acc:7.0, topSpeed:239, engine: '525d', price: '$13.590', img: '/static/images/bmw525.png', rearImg: '/static/rearimg/bmw525-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id:'550',              name: '2026 BMW 550',       power:489, acc:4.4, topSpeed:250, engine: '550e', price: '$77.750', img: '/static/images/bmw550.jpg', rearImg: '/static/rearimg/bmw550-rear.jpg' , consumption: { value:23.0, unit: 'kWh/100km' }},

  { id:'620',              name: '2021 BMW 620',       power:190, acc:7.9, topSpeed:220, engine: '620d', price: '$32.990', img: '/static/images/bmw620.png', rearImg: '/static/rearimg/bmw620-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id:'635',              name: '2010 BMW 635',       power:287, acc:6.6, topSpeed:250, engine: '635d', price: '$14.990', img: '/static/images/bmw635.jpg', rearImg: '/static/rearimg/bmw635-rear.jpg' , consumption: { value:8.5, unit: 'L/100km' }},

  { id:'i4',               name: '2025 BMW i4',        power:544, acc:3.9, topSpeed:225, engine: 'M50 83.9 kWh', price: '$53.770', img: '/static/images/bmwi4.jpg', rearImg: '/static/rearimg/bmwi4-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }, addedAt: '2026-03-12T09:00:00Z' },

  { id: 'M1',              name: '2024 BMW M1',        power:300, acc:4.9, topSpeed:250, engine: 'M135 xDrive Steptronic DCT', price: '$43.960', img: '/static/images/bmwM1.jpg', rearImg: '/static/rearimg/bmwM1-rear.png' , consumption: { value:8.5, unit: 'L/100km' }},
  
  { id: 'M2',              name: '2024 BMW M2',        power:530, acc:3.8, topSpeed:302, engine: 'CS 3.0 M Steptronic', price: '$124.405', img: '/static/images/bmwM2.jpg', rearImg: '/static/rearimg/bmwM2-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'M3',              name: '2024 BMW M3',        power:530, acc:3.6, topSpeed:250, engine: 'Competition 3.0 M xDrive M Steptronic', price: '$99.900', img: '/static/images/bmwM3.jpg', rearImg: '/static/rearimg/bmwM3-rear.jpg' , consumption: { value:10.5, unit: 'L/100km' }},

  { id: 'M4',              name: '2024 BMW M4',        power:530, acc:3.4, topSpeed:302, engine: 'CS 3.0 M xDrive M Steptronic', price: '$134.990', img: '/static/images/bmwM4.jpg', rearImg: '/static/rearimg/bmwM4-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'M5',              name: '2024 BMW M5',        power:726, acc:3.5, topSpeed:250, engine: '4.4 V8 Plug-in Hybrid M xDrive M Steptronic', price: '$129.950', img: '/static/images/bmwM5.jpg', rearImg: '/static/rearimg/bmwM5-rear.jpg' , consumption: { value:25, unit: 'kWh/100km' }},

  { id: 'M5 CS',           name: '2022 BMW M5',        power:635, acc:3.0, topSpeed:305, engine: 'CS 4.4 V8 xDrive Steptronic', price: '$142.995', img: '/static/images/bmwM5CS.jpg', rearImg: '/static/rearimg/bmwM5CS-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'M6',              name: '2017 BMW M6',        power:600, acc:3.9, topSpeed:250, engine: 'Competition 4.4 V8 M DCT', price: '$69.890', img: '/static/images/bmwM6.jpg', rearImg: '/static/rearimg/bmwM6-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'M8',              name: '2022 BMW M8',        power:625, acc:3.2, topSpeed:250, engine: 'Competition 4.4 V8 xDrive Steptronic Sport', price: '$139.890', img: '/static/images/bmwM8.jpg', rearImg: '/static/rearimg/bmwM8-rear.jpg' , consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'İ7',              name: '2024 BMW i7',        power:660, acc:3.7, topSpeed:250, engine: 'M70 105.7 kWh xDrive', price: '$85.900', img: '/static/images/bmwİ7.jpg', rearImg: '/static/rearimg/bmwİ7-rear.jpg' , consumption: { value:23.5, unit: 'kWh/100km' }},

  { id: 'X3',              name: '2024 BMW X3',        power:398, acc:3.8, topSpeed:250, engine: 'M xDrive M Steptronic', price: '$67.900', img: '/static/images/bmwX3.jpg', rearImg: '/static/rearimg/bmwX3-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Z4',              name: '2024 BMW Z4',        power:340, acc:4.5, topSpeed:250, engine: 'M40i 3.0', price: '$68.900', img: '/static/images/bmwZ4.png', rearImg: '/static/rearimg/bmwZ4-rear.png', consumption: { value:8.0, unit: 'L/100km' }, addedAt: '2026-03-11T09:00:00Z' },

  { id: 'X5',              name: '2024 BMW X5',        power:381, acc:3.9, topSpeed:250, engine: '40i xDrive', price: '$74.600', img: '/static/images/bmwX5.jpg', rearImg: '/static/rearimg/bmwX5-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'iX',              name: '2024 BMW iX',        power:516, acc:4.6, topSpeed:200, engine: 'xDrive50 111.5 kWh', price: '$87.250', img: '/static/images/bmwIX.png', rearImg: '/static/rearimg/bmwIX-rear.png', consumption: { value:22.0, unit: 'kWh/100km' }, addedAt: '2026-03-10T09:00:00Z' },

  { id: 'X6 M',            name: '2022 BMW X6 M',      power:625, acc:3.8, topSpeed:250, engine: '4.4 V8  xDrive Steptronic', price: '$79.900', img: '/static/images/bmwX6M.jpg', rearImg: '/static/rearimg/bmwX6M-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'X7 M',            name: '2020 BMW X7 M',      power:530, acc:4.7, topSpeed:250, engine: 'M50i V8 xDrive Steptronic', price: '$67.490', img: '/static/images/bmwX7M.jpg', rearImg: '/static/rearimg/bmwX7M-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'X7',              name: '2024 BMW X7',        power:352, acc:4.7, topSpeed:250, engine: 'xdrive 40d 48V MSport', price: '$84.900', img: '/static/images/bmwX7.jpg', rearImg: '/static/rearimg/bmwX7-rear.png' , consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'XM',              name: '2024 BMW XM',        power:476, acc:5.1, topSpeed:250, engine: '50e Plug-in Hybrid M xDrive M Steptronic', price: '$109.900', img: '/static/images/bmwXM.jpg', rearImg: '/static/rearimg/bmwXM-rear.png' , consumption: { value:30, unit: 'kWh/100km' }},

  { id: 'AMG GT',          name: '2024 Mercedes-Benz AMG GT', power:816, acc:2.8, topSpeed:320, engine: '63 S E PERFORMANCE V8', price: '$199,900', img: '/static/images/mercedesAMGGT.jpg', rearImg: '/static/rearimg/mercedesAMGGT-rear.png'  , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'AMG ONE',         name: '2025 Mercedes-Benz AMG ONE', power:1063, acc:2.9, topSpeed:352, engine: '1.6 V6 E PERFORMANCE', price: '$3,387,950', img: '/static/images/mercedesAMGONE.jpg', rearImg: '/static/rearimg/mercedesAMGONE-rear.png' , consumption: { value:35, unit: 'L/100km' }},

  { id: 'C 63 AMG',        name: '2014 Mercedes-Benz C 63 AMG', power:507, acc:4.2, topSpeed:280, engine: 'AMG C 63 AMG Edition V8', price: '$91,507', img: '/static/images/mercedesC63AMG.jpg', rearImg: '/static/rearimg/mercedesC63AMG-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'C 63 AMG 2',      name: '2020 Mercedes-Benz C 63 AMG', power:510, acc:4.0, topSpeed:280, engine: '4.0 L V8 Biturbo', price: '$63.950', img: '/static/images/mercedesC63AMG2.jpg', rearImg: '/static/rearimg/mercedesC63AMG2-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'CLK 63 AMG',      name: '2008 Mercedes-Benz CLK 63 AMG', power:507, acc:4.3, topSpeed:300, engine: 'AMG CLK 63 Black Series V8 7G-TRONIC AMG SPEEDSHIFT', price: '$118,990', img: '/static/images/mercedesCLK63AMG.jpg', rearImg: '/static/rearimg/mercedesCLK63AMG-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'CLS 63 AMG',      name: '2011 Mercedes-Benz CLS 63 AMG', power:525, acc:4.4, topSpeed:250, engine: 'AMG CLS 63 V8 AMG SPEEDSHIFT MCT', price: '$37,999', img: '/static/images/mercedesCLS63AMG.jpg', rearImg: '/static/rearimg/mercedesCLS63AMG-rear.jpg' , consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'CLS 63 AMG 2',    name: '2016 Mercedes-Benz CLS 63 AMG', power:585, acc:3.7, topSpeed:250, engine: 'AMG CLS 63 S V8 MCT 4MATIC', price: '$56,490', img: '/static/images/mercedesCLS63AMG2.jpg', rearImg: '/static/rearimg/mercedesCLS63AMG2-rear.jpg' , consumption: { value:12.5, unit: 'L/100km' }},

  { id: 'E 53 AMG',        name: '2025 Mercedes-Benz E 53 AMG', power:612, acc:3.8, topSpeed:280, engine: 'AMG E 53 HYBRID 4Matic+ AMG', price: '$107,999', img: '/static/images/mercedesE53AMG.png', rearImg: '/static/rearimg/mercedesE53AMG-rear.png' , consumption: { value:8.5, unit: 'L/100km' }},

  { id: 'G 55 AMG',        name: '2010 Mercedes-Benz G 55 AMG', power:507, acc:5.5, topSpeed:210, engine: 'AMG G 55 V8 Kompressor', price: '$70,500', img: '/static/images/mercedesG55AMG.jpg', rearImg: '/static/rearimg/mercedesG55AMG-rear.jpg' , consumption: { value:18.5, unit: 'L/100km' }},

  { id: 'G',               name: '2025 Mercedes-Benz G', power:585, acc:4.4, topSpeed:220, engine: 'AMG G 63 V8 Mild Hybrid 4MATIC AMG SPEEDSHIFT TCT 9G', price: '$269,990', img: '/static/images/mercedesG.jpg', rearImg: '/static/rearimg/mercedesG-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'GLS 63 AMG',      name: '2023 Mercedes-Benz GLS 63 AMG', power:612, acc:4.2, topSpeed:250, engine: 'AMG GLS 63 V8 Mild Hybrid 4MATIC', price: '$182,100', img: '/static/images/mercedesGLS63AMG.jpg', rearImg: '/static/rearimg/mercedesGLS63AMG-rear.png' , consumption: { value:13.5, unit: 'L/100km' }},

  { id: 'GLE',             name: '2024 Mercedes-Benz GLE', power:375, acc:5.6, topSpeed:250, engine: '450 4MATIC 3.0', price: '$69.500', img: '/static/images/mercedesGLE450.jpg', rearImg: '/static/rearimg/mercedesGLE450-rear.png', consumption: { value:9.8, unit: 'L/100km' }},

  { id: 'GLC',             name: '2024 Mercedes-Benz GLC', power:255, acc:6.2, topSpeed:240, engine: '300 4MATIC 2.0', price: '$51.400', img: '/static/images/mercedesGLC300.png', rearImg: '/static/rearimg/mercedesGLC300-rear.png', consumption: { value:8.3, unit: 'L/100km' }},

  { id: 'GLS',             name: '2024 Mercedes-Benz GLS', power:375, acc:6.1, topSpeed:246, engine: '450 4MATIC 3.0', price: '$88.150', img: '/static/images/mercedesGLS450.png', rearImg: '/static/rearimg/mercedesGLS450-rear.png', consumption: { value:10.5, unit: 'L/100km' }},

  { id: 'EQE SUV',         name: '2024 Mercedes-Benz EQE SUV', power:402, acc:5.4, topSpeed:210, engine: '96 kWh', price: '$79.050', img: '/static/images/mercedesEQESUV.jpg', rearImg: '/static/rearimg/mercedesEQESUV-rear.jpg', consumption: { value:21.5, unit: 'kWh/100km' }},

  { id: 'Maybach GLS',     name: '2025 Mercedes-Benz Maybach GLS', power:557, acc:4.9, topSpeed:250, engine: 'GLS 600 V8 Mild Hybrid 4MATIC 9G-TRONIC', price: '$220,150', img: '/static/images/mercedesMaybachGLS.jpg', rearImg: '/static/rearimg/mercedesMaybachGLS-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Maybach S-Klasse', name: '2025 Mercedes-Benz Maybach S-Klasse', power:612, acc:4.5, topSpeed:250, engine: 'Maybach S680 BRABUS 4Matic + Burmester', price: '$270,130', img: '/static/images/mercedesMaybach S-Klasse.jpg', rearImg: '/static/rearimg/mercedesMaybach S-Klasse-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'SL Roadster AMG',  name: '2023 Mercedes-Benz SL Roadster AMG', power:816, acc:2.9, topSpeed:317, engine: 'AMG SL 63 S E PERFORMANCE V8  Plug-in Hybrid 4MATIC', price: '$156,875', img: '/static/images/mercedesSL Roadster AMG.png', rearImg: '/static/rearimg/mercedesSL Roadster AMG-rear.png' , consumption: { value:19.5, unit: 'kWh/100km' }},

  { id: 'SLC',              name: '2020 Mercedes-Benz SLC', power:362, acc:4.7, topSpeed:250, engine: 'AMG SLC 43 3.0 V6', price: '$54.900', img: '/static/images/mercedesSLC43AMG.png', rearImg: '/static/rearimg/mercedesSLC43AMG-rear.png', consumption: { value:9.4, unit: 'L/100km' }},

  { id: 'SLR',              name: '2007 Mercedes-Benz SLR', power:650, acc:3.6, topSpeed:337, engine: '722 Edition 5.5 V8 Kompressor AMG SPEEDSHIFT R', price: '$729,890', img: '/static/images/mercedesSLR.jpg', rearImg: '/static/rearimg/mercedesSLR-rear.png' , consumption: { value:19.5, unit: 'L/100km' }},

  { id: 'SLR 2',            name: '2011 Mercedes-Benz SLR', power:650, acc:3.5, topSpeed:350, engine: '5.5 V8 Kompressor AMG SPEEDSHIFT R', price: '$2,889,000', img: '/static/images/mercedesSLR2.jpg', rearImg: '/static/rearimg/mercedesSLR2-rear.png' , consumption: { value:20.5, unit: 'L/100km' }},

  { id: 'SLS',             name: '2012 Mercedes-Benz SLS', power:591, acc:3.7, topSpeed:320, engine: 'FINAL EDITION GT 6.2 V8  AMG SPEEDSHIFT DCT', price: '$229,900', img: '/static/images/mercedesSLS.jpg', rearImg: '/static/rearimg/mercedesSLS-rear.png' , consumption: { value:15.5, unit: 'L/100km' }},

  { id: 'X 350',           name: '2020 Mercedes-Benz X 350', power:258, acc:7.9, topSpeed:205, engine: 'X 350d V6', price: '$48,990', img: '/static/images/mercedesX350.png', rearImg: '/static/rearimg/mercedesX350-rear.png' , consumption: { value:9.5, unit: 'L/100km' }},

  { id: 'NSX',             name: '2022 Acura NSX', power:600, acc:3, topSpeed:307, engine: 'Type S 3.5 V6 Hybrid SH-AWD DCT', price: '$200.500', img: '/static/images/acuraNSX.jpg' , rearImg: '/static/rearimg/acuraNSX-rear.jpg' , consumption: { value:22.0, unit: 'kWh/100km' }},

  { id: 'NSX 2',           name: '1991 Acura NSX', power:256, acc:5.9, topSpeed:260, engine: '3.0 i V6 24V', price: '$150.000', img: '/static/images/acuraNSX2.jpg', rearImg: '/static/rearimg/acuraNSX2-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'MDX',             name: '2024 Acura MDX', power:355, acc:5.5, topSpeed:180, engine: 'Type S 3.0 Turbo V6', price: '$73.500', img: '/static/images/acuraMDX.jpg', rearImg: '/static/rearimg/acuraMDX-rear.jpg', consumption: { value:11.2, unit: 'L/100km' }},

  { id: 'RDX',             name: '2024 Acura RDX', power:272, acc:6.4, topSpeed:180, engine: '2.0 Turbo SH-AWD', price: '$46.050', img: '/static/images/acuraRDX.jpg', rearImg: '/static/rearimg/acuraRDX-rear.jpg', consumption: { value:9.6, unit: 'L/100km' }},

  { id: '8C',              name: '2009 Alfa Romeo 8C', power:450, acc:4.4, topSpeed:290, engine: '4.7 V8', price: '$335.000', img: '/static/images/alfaromeo8c.jpg', rearImg: '/static/rearimg/alfaromeo8c-rear.jpg' , consumption: { value:13.5, unit: 'L/100km' }},

  { id: '33',              name: '2024 Alfa Romeo 33', power:620, acc:3.0, topSpeed:333, engine: '3.0 V6 DCT', price: '$3.500.000', img: '/static/images/alfaromeo33.jpg', rearImg: '/static/rearimg/alfaromeo33-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Giulia',          name: '2024 Alfa Romeo Giulia', power:540, acc:3.9, topSpeed:308, engine: 'Quadrifoglio 2.9 V6 Bi-Turbo', price: '$220.000', img: '/static/images/alfaromeoGiulia.jpg', rearImg: '/static/rearimg/alfaromeoGiulia-rear.jpg' , consumption: { value:10.5, unit: 'L/100km' }},

  { id: 'Stelvio',         name: '2024 Alfa Romeo Stelvio', power:280, acc:5.7, topSpeed:230, engine: '2.0 Turbo Q4', price: '$50.990', img: '/static/images/alfaromeoStelvio.jpg', rearImg: '/static/rearimg/alfaromeoStelvio-rear.png', consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'A110',            name: '2024 Alpine A110', power:300, acc:4.2, topSpeed:260, engine: 'S 1.8 DCT', price: '$81.950', img: '/static/images/alpineA110.jpg', rearImg: '/static/rearimg/alpineA110-rear.jpg' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'DB',              name: '2025 Aston Martin DB', power:680, acc:3.6, topSpeed:325, engine: '4.0 V8', price: '$210.000', img: '/static/images/astonmartinDB.jpg', rearImg: '/static/rearimg/astonmartinDB-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'DB7',             name: '1995 Aston Martin DB7', power:360, acc:6, topSpeed:265, engine: '3.2', price: '$38.500', img: '/static/images/astonmartinDB7.jpg', rearImg: '/static/rearimg/astonmartinDB7-rear.png' , consumption: { value:14.5, unit: 'L/100km' }},

  { id: 'DB9',             name: '2004 Aston Martin DB9', power:456, acc:5.1, topSpeed:300, engine: '6.0 i V12 48V', price: '$59.990', img: '/static/images/astonmartinDB9.jpg', rearImg: '/static/rearimg/astonmartinDB9-rear.jpg' , consumption: { value:15.5, unit: 'L/100km' }},

  { id: 'DBS',             name: '2024 Aston Martin DBS', power:770, acc:3.6, topSpeed:340, engine: 'Ultimate 5.2 V12', price: '$399.000', img: '/static/images/astonmartinDBS.jpg', rearImg: '/static/rearimg/astonmartinDBS-rear.jpg' , consumption: { value:13.5, unit: 'L/100km' }},

  { id: 'DBX',             name: '2024 Aston Martin DBX', power:727, acc:3.3, topSpeed:310, engine: 'S 4.0 V8', price: '$174.900', img: '/static/images/astonmartinDBX.jpg', rearImg: '/static/rearimg/astonmartinDBX-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Lagonda',         name: '2015 Aston Martin Lagonda', power:548, acc:4.4, topSpeed:320, engine: '5.9 L V12', price: '$773.500', img: '/static/images/astonmartinLagonda.png', rearImg: '/static/rearimg/astonmartinLagonda-rear.jpg' , consumption: { value:13.5, unit: 'L/100km' }},

  { id: 'Rapide',          name: '2019 Aston Martin Rapide', power:559, acc:4.4, topSpeed:330, engine: '6.0 V12', price: '$114.950', img: '/static/images/astonmartinRapide.png', rearImg: '/static/rearimg/astonmartinRapide-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'V8',              name: '2024 Aston Martin V8', power:536, acc:3.5, topSpeed:325, engine: '4.0 V8', price: '$148.000', img: '/static/images/astonmartinV8.png', rearImg: '/static/rearimg/astonmartinV8-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Valkyrie',        name: '2024 Aston Martin Valkyrie', power:1156, acc:2.5, topSpeed:400, engine: '6.5L V12 Hybrid', price: '$3.600.000', img: '/static/images/astonmartinValkyrie.jpg'  , rearImg: '/static/rearimg/astonmartinValkyrie-rear.jpg' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Valour',          name: '2024 Aston Martin Valour', power:715, acc:3.0, topSpeed:322, engine: '5.2 V12', price: '$2.050.000', img: '/static/images/astonmartinValour.jpg', rearImg: '/static/rearimg/astonmartinValour-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Vanquish',        name: '2025 Aston Martin Vanquish', power:835, acc:3.4, topSpeed:345, engine: '5.2 V12 ZF', price: '$435.000', img: '/static/images/astonmartinVanquish.png', rearImg: '/static/rearimg/astonmartinVanquish-rear.jpg' , consumption: { value:14.5, unit: 'L/100km' }},

  { id: 'Volante',         name: '2025 Aston Martin Volante', power:689, acc:3.7, topSpeed:318, engine: 'V8 4.0 680ch BVA8', price: '$295.000', img: '/static/images/astonmartinVolante.png', rearImg: '/static/rearimg/astonmartinVolante-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Arnage',          name: '2005 Bentley Arnage', power:405 , acc:7, topSpeed:250, engine: 'Arnage RL 6.75 Turbo V8 phase II', price: '$42.000', img: '/static/images/bentleyArnage.png', rearImg: '/static/rearimg/bentleyArnage-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Azure',           name: '2007 Bentley Azure', power:457, acc:6, topSpeed:270, engine: '6.7 i V8', price: '$129.900', img: '/static/images/bentleyAzure.png', rearImg: '/static/rearimg/bentleyAzure-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Bentayga',        name: '2024 Bentley Bentayga', power:549, acc:4.6, topSpeed:290, engine: '4.0 V8', price: '$200.000', img: '/static/images/bentleyBentayga.png', rearImg: '/static/rearimg/bentleyBentayga-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Continental',     name: '2025 Bentley Continental', power:782, acc:3.4, topSpeed:285, engine: '4.0 V8 TFSi Ultra Performance Hybrid AWD DCT', price: '$330.000', img: '/static/images/bentleyContinental.png', rearImg: '/static/rearimg/bentleyContinental-rear.jpg' , consumption: { value:23.0, unit: 'kWh/100km' }},

  { id: 'Batur',           name: '2024 Bentley Batur', power:744, acc:3.0, topSpeed:336, engine: '6.0 i W12,', price:'$2.552.550', img: '/static/images/bentleyBatur.jpg', rearImg: '/static/rearimg/bentleyBatur-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'CR 4',            name: '2024 Boldmen CR 4', power:408, acc:3.9, topSpeed:300, engine: '3.0 Inline-6 Turbo', price: '$199.985', img: '/static/images/boldmenCR4.png', rearImg: '/static/rearimg/boldmenCR4-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'Veyron',          name: '2013 Bugatti Veyron', power:1001, acc:2.6, topSpeed:410, engine: 'Grand Sport Vitesse 8.0 W16', price: '$2.290.000', img: '/static/images/bugattiVeyron.png', rearImg: '/static/rearimg/bugattiVeyron-rear.jpg' , consumption: { value:24.0, unit: 'L/100km' }},

  { id: 'Chiron',          name: '2022 Bugatti Chiron', power:1500, acc:2.4, topSpeed:440, engine: '8.0 W16', price: '$5.100.000', img: '/static/images/bugttiChiron.jpg', rearImg: '/static/rearimg/bugttiChiron-rear.jpg' , consumption: { value:24.0, unit: 'L/100km' }},

  { id: 'Divo',            name: '2020 Bugatti Divo', power:1500, acc:2.4, topSpeed:380, engine: '8.0 W16', price: '$13.500.000', img: '/static/images/bugattiDivo.png', rearImg: '/static/rearimg/bugattiDivo-rear.jpg' , consumption: { value:24.0, unit: 'L/100km' }},

  { id: 'EB 110',          name: '1995 Bugatti EB 110', power:560, acc:3.4, topSpeed:350, engine: 'GT SS', price: '$2.750.000', img: '/static/images/bugattiEB110.png', rearImg: '/static/rearimg/bugattiEB110-rear.jpg' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Yangwang U9',     name: '2024 BYD Yangwang U9', power:1305, acc:2.36, topSpeed:309, engine: 'U9', price: '$297.500', img: '/static/images/bydYangwangu9.png', rearImg: '/static/rearimg/bydYangwangu9-rear.jpg' , consumption: { value:28.0, unit: 'kWh/100km' }},

  { id: 'ATS',             name: '2019 Cadillac ATS', power:470, acc:4.2, topSpeed:298, engine: 'V 3.6 V6', price: '$49.900', img: '/static/images/cadillacAts.jpg', rearImg: '/static/rearimg/cadillacAts-rear.jpg' , consumption: { value:9.5, unit: 'L/100km' }},

  { id: 'CT4',             name: '2025 Cadillac CT4', power:472, acc:4.0, topSpeed:304, engine: 'V Blackwing 3.6 V6', price: '$105.000', img: '/static/images/cadillacCt4.jpg', rearImg: '/static/rearimg/cadillacCt4-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'CT5',             name: '2025 Cadillac CT5', power:677, acc:3.7, topSpeed:322, engine: 'V Blackwing 6.2 V8', price: '$169.000', img: '/static/images/cadillacCt5.jpg', rearImg: '/static/rearimg/cadillacCt5-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Escalade',        name: '2024 Cadillac Escalade', power:681, acc:4.4, topSpeed:200, engine: '6.2L V8 Supercharged', price: '$198.500', img: '/static/images/cadillacEscalade.jpg', rearImg: '/static/rearimg/cadillacEscalade-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'Lyriq',           name: '2024 Cadillac Lyriq', power:528, acc:4.9, topSpeed:190, engine: 'Dual Electric Motor 102 kWh Battery', price: '$64.950', img: '/static/images/cadillacLyriq.png', rearImg: '/static/rearimg/cadillacLyriq-rear.jpg' , consumption: { value:22.5, unit: 'kWh/100km' }},

  { id: 'Camaro',          name: '2022 Chevrolet Camaro', power:659, acc:3.5, topSpeed:318, engine: '6.2L V8 Supercharged', price: '$64.990', img: '/static/images/chevroletCamaro.png', rearImg: '/static/rearimg/chevroletCamaro-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Camaro SS',       name: '2022 Chevrolet Camaro SS', power:455, acc:4.0, topSpeed:290, engine: '6.2L V8', price: '$45.295', img: '/static/images/chevroletCamaro.png', rearImg: '/static/rearimg/chevroletCamaro-rear.png' , consumption: { value:12.4, unit: 'L/100km' }},

  { id: 'Chevelle',        name: '1970 Chevrolet Chevelle', power:351, acc:6.0, topSpeed:210, engine: '6.5L V8 Big Block', price: '$45.900', img: '/static/images/chevroletChevelle.jpg', rearImg: '/static/rearimg/chevroletChevelle-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Corvette',        name: '2025 Chevrolet Corvette', power:502, acc:3.0, topSpeed:312, engine: '6.2L V8 NA', price: '$139.900', img: '/static/images/chevroletCorvette.jpg', rearImg: '/static/rearimg/chevroletCorvette-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'Tahoe',           name: '2025 Chevrolet Tahoe', power:426, acc:5.9, topSpeed:210, engine: '6.2L V8 NA', price: '$88.000', img: '/static/images/chevroletTahoe.png', rearImg: '/static/rearimg/chevroletTahoe-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: '300 SRT',         name: '2013 Chrysler 300 SRT', power:479, acc:4.5, topSpeed:250, engine: '6.4L V8 HEMI', price: '$39.950', img: '/static/images/chrysler300SRT.png', rearImg: '/static/rearimg/chrysler300SRT-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Cirelli 3',       name: '2025 Cirelli Cirelli 3', power:133, acc:11.0, topSpeed:180, engine: '1.5 turbo', price: '$23.800', img: '/static/images/cirellicirelli3.png', rearImg: '/static/rearimg/cirellicirelli3-rear.webp' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Cirelli 4',       name: '2025 Cirelli Cirelli 4', power:184, acc:9.2, topSpeed:195, engine: '1.5L turbo', price: '$30.800', img: '/static/images/cirellicirelli4.png', rearImg: '/static/rearimg/cirellicirelli4-rear.webp' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Cirelli 7',       name: '2024 Cirelli Cirelli 5', power:177, acc:9.4, topSpeed:200, engine: '1.5 Premium', price: '$31.800', img: '/static/images/cirelliCirelli7.png', rearImg: '/static/rearimg/cirelliCirelli7-rear.webp' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Ami',             name: '2024 Citroen Ami', power:8, acc:0, topSpeed:45, engine: 'Sport', price: '$7.500', img: '/static/images/citroenAmi.png', rearImg: '/static/rearimg/citroenAmi-rear.webp' , consumption: { value:9.0, unit: 'kWh/100km' }},

  { id: 'C-Elysée',        name: '2018 Citroen C-Elysée', power:116, acc:11.1, topSpeed:193, engine: '1.6 VTi', price: '$10.000', img: '/static/images/citroenCelysée.png', rearImg: '/static/rearimg/citroenCelysee-rear.png' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'E-C4 X',          name: '2024 Citroen E-C4 X', power:132, acc:10.3, topSpeed:210, engine: '1.5 L BlueHDi', price: '$19.950', img: '/static/images/citroenEC4X.png', rearImg: '/static/rearimg/citroenEC4X-rear.png' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'DS',              name: '2025 Citroen DS', power:230, acc:7.7, topSpeed:190, engine: 'ÉTOILE 74kWh', price: '$69.199', img: '/static/images/citroenDS.png', rearImg: '/static/rearimg/citroenDS-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'DS3',             name: '2022 Citroen DS3', power:136, acc:9.0, topSpeed:150, engine: 'E-TENSE', price: '$21.990', img: '/static/images/citroenDS3.png', rearImg: '/static/rearimg/citroenDS3-rear.png' , consumption: { value:5.0, unit: 'L/100km' }},

  { id: 'DS4',             name: '2023 Citroen DS4', power:131, acc:9.6, topSpeed:210, engine: '1.2 PureTech Turbo', price: '$22.470', img: '/static/images/citroenDS4.png', rearImg: '/static/rearimg/citroenDS4-rear.jpg' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'C2',              name: '1966 Corvette C2', power:351, acc:5.5, topSpeed:245, engine: '7.0L V8 Turbo-Jet', price: '$72.000', img: '/static/images/corvetteC2.png', rearImg: '/static/rearimg/corvetteC2-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'C3',              name: '1971 Corvette C3', power:286, acc:6.8, topSpeed:225, engine: '5.7 L V8', price: '$24.900', img: '/static/images/corvetteC3.jpg', rearImg: '/static/rearimg/corvetteC3-rear.webp' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'C4',              name: '1995 Corvette C4', power:306, acc:5.5, topSpeed:260, engine: '5.7L V8 LT1', price: '$23.900', img: '/static/images/corvetteC4.png', rearImg: '/static/rearimg/corvetteC4-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'C5',              name: '2000 Corvette C5', power:355, acc:4.8, topSpeed:273, engine: '5.7 i V8 16V', price: '$35.995', img: '/static/images/corvetteC5.png', rearImg: '/static/rearimg/corvetteC5-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'C6 Convertible',  name: '2008 Corvette C6', power:404, acc:4.2, topSpeed:290, engine: '6.0 i V8', price: '$39.975', img: '/static/images/corvetteC6.jpg', rearImg: '/static/rearimg/corvetteC6-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'C7',              name: '2019 Corvette C7', power:466 , acc:4.2, topSpeed:290, engine: 'V8 6.2 2LT AT8', price: '$79.900', img: '/static/images/corvetteC7.png', rearImg: '/static/rearimg/corvetteC7-rear.jpg' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'C8',              name: '2025 Corvette C8', power:495, acc:3.5, topSpeed:296, engine: 'Stingray 6.2 V8', price: '$119.969', img: '/static/images/corvetteC8.png', rearImg: '/static/rearimg/corvetteC8-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Ateca',           name: '2025 CUPRA Ateca', power:247, acc:9.3, topSpeed:199, engine: '1.5 TSI', price: '$42.490', img: '/static/images/cupraateca.png', rearImg: '/static/rearimg/cupraateca-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Born',            name: '2025 CUPRA Born', power:231, acc:6.6, topSpeed:160, engine: 'e-Boost 62 kWh', price: '$33.680', img: '/static/images/cupraBorn.png', rearImg: '/static/rearimg/cupraBorn-rear.jpg' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'Leon',            name: '2023 CUPRA Leon', power:245, acc:6.6, topSpeed:250, engine: '2.0 TSI', price: '$23,480', img: '/static/images/cupraLeon.png', rearImg: '/static/rearimg/cupraLeon-rear.jpg' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Tavascan',        name: '2024 CUPRA Tavascan', power:286, acc:6.8, topSpeed:180, engine: '82 kWh', price: '$39,890', img: '/static/images/cupraTavascan.png', rearImg: '/static/rearimg/cupraTavascan-rear.jpg' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Terramar',        name: '2025 CUPRA Terramar', power:265, acc:5.9, topSpeed:243, engine: '2.0 TSI', price: '$33,470', img: '/static/images/cupraTerramar.png', rearImg: '/static/rearimg/cupraTerramar-rear.png' , consumption: { value:7.5, unit: 'L/100km' }},

  { id: 'Bigster',         name: '2025 Dacia Bigster', power:158, acc:9.7, topSpeed:180, engine: '1.8 Hybrid Automatic', price: '$29,870', img: '/static/images/daciaBigster.png', rearImg: '/static/rearimg/daciaBigster-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: 'Spring',          name: '2023 Dacia Spring', power:45, acc:19.1, topSpeed:125, engine: '27.4 kWh', price: '$11,390', img: '/static/images/daciaSpring.png', rearImg: '/static/rearimg/daciaSpring-rear.png' , consumption: { value:14.0, unit: 'kWh/100km' }},

  { id: 'Guarà',           name: '1995 De Tomaso Guarà', power:286, acc:5.0, topSpeed:270, engine: '4.0 L V8', price: '$230,000', img: '/static/images/detomasoGuara.png', rearImg: '/static/rearimg/detomasoGuara-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'Mangusta',        name: '1970 De Tomaso Mangusta', power:305, acc:6.0, topSpeed:250, engine: '4.7 L V8', price: '$330,000', img: '/static/images/detomasoMangusta.png', rearImg: '/static/rearimg/detomasoMangusta-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Pantera',         name: '1971 De Tomaso Pantera', power:330, acc:5.5, topSpeed:269, engine: '5.0 V8', price: '$140,000', img: '/static/images/detamasoPantera.png', rearImg: '/static/rearimg/detamasoPantera-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'DMC-12',         name: '1981 Delorean DMC-12', power:132, acc:9.5, topSpeed:175, engine: '2.85 L V6', price: '$75,900', img: '/static/images/deloreanDMC12.png', rearImg: '/static/rearimg/deloreanDMC12-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Fengon',         name: '2025 DFSK Fengon', power:177, acc:7.4, topSpeed:165, engine: 'DE-i 1.5', price: '$27,995', img: '/static/images/dfskFengon.png', rearImg: '/static/rearimg/dfskFengon-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Forthing 5',     name: '2025 DFSK Forthing 5', power:177, acc:9.5, topSpeed:190, engine: '1.5 L Turbo', price: '$25,690', img: '/static/images/dfskForthing5.png', rearImg: '/static/rearimg/dfskForthing5-rear.png' , consumption: { value:7.5, unit: 'L/100km' }},

  { id: 'Challenger',     name: '2018 Dodge Challenger', power:807, acc:3.7, topSpeed:270, engine: 'SRT Super Stock 6.2 HEMI V8', price: '$80,500', img: '/static/images/dodgeChallenger.png', rearImg: '/static/rearimg/dodgeChallenger-rear.jpg' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'Charger',        name: '2025 Dodge Charger', power:727, acc:3.6, topSpeed:327, engine: '6.2 L Supercharged V8', price: '$84,990', img: '/static/images/dodgeCharger.png', rearImg: '/static/rearimg/dodgeCharger-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Coronet',        name: '1968 Dodge Coronet', power:375, acc:5.5, topSpeed:230, engine: '7.2L V8', price: '$70,000', img: '/static/images/dodgeCoronet.png', rearImg: '/static/rearimg/dodgeCoronet-rear.jpg' , consumption: { value:21.0, unit: 'L/100km' }},

  { id: 'Demon',          name: '2018 Dodge Demon', power:840, acc:2.3, topSpeed:270, engine: '6.2 L Supercharged V8 (HEMI)', price: '$329,000', img: '/static/images/dodgeDemon.png', rearImg: '/static/rearimg/dodgeDemon-rear.png' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'Durango',        name: '2023 Dodge Durango', power:702, acc:3.5, topSpeed:290, engine: '6.2L Supercharged V8', price: '$75,000', img: '/static/images/dodgeDurango.png', rearImg: '/static/rearimg/dodgeDurango-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'RAM',            name: '2024 Dodge RAM', power:711, acc:4.5, topSpeed:190, engine: '6.2L Supercharged V8', price: '$163,229', img: '/static/images/dodgeRAM.png', rearImg: '/static/rearimg/dodgeRAM-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Viper',          name: '2017 Dodge Viper', power:650, acc:3.9, topSpeed:325, engine: 'SRT 8.4i V10 20V', price: '$259,000', img: '/static/images/dodgeViper.png', rearImg: '/static/rearimg/dodgeViper-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'D8',             name: '2023 Donkervoort D8', power:360, acc:2.7, topSpeed:280, engine: '2.0 L Turbo', price: '$212,070', img: '/static/images/donkervoortD8.png', rearImg: '/static/rearimg/donkervoortD8-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'F22',            name: '2024 Donkervoort F22', power:500, acc:2.5, topSpeed:290, engine: '2.5L Turbo', price: '$389.900', img: '/static/images/donkervoortF22.png', rearImg: '/static/rearimg/donkervoortF22-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'DS 7',           name: '2024 DS Automobiles DS 7', power:131, acc:10.9, topSpeed:195, engine: '1.5 Opera', price: '$28.975', img: '/static/images/dsautomobilesds7.png', rearImg: '/static/rearimg/dsautomobilesds7-rear.jpg' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'DS 9',           name: '2024 DS Automobiles DS 9', power:200, acc:8.1, topSpeed:200, engine: '1.6 Plug-In', price: '$39.950', img: '/static/images/dsautomobilesds9.png', rearImg: '/static/rearimg/dsautomobilesds9-rear.png' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'N°4',            name: '2025 DS Automobiles N°4', power:136, acc:8.4, topSpeed:210, engine: '1.2L Turbo', price: '$45.550', img: '/static/images/dsautomobilesN4.png', rearImg: '/static/rearimg/dsautomobilesN4-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'N°8',            name: '2025 DS Automobiles N°8', power:245, acc:7.5, topSpeed:190, engine: 'Dual Electric Motor', price: '$66.950', img: '/static/images/dsautomobilesN8.png', rearImg: '/static/rearimg/dsautomobilesN8-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 's700',           name: '2025 Ebro s700', power:147, acc:9.8, topSpeed:190, engine: '1.6L Turbo', price: '$23.500', img: '/static/images/ebroS700.png', rearImg: '/static/rearimg/ebroS700-rear.png' , consumption: { value:8.5, unit: 'L/100km' }},

  { id: 'Beo',            name: '2024 Elaris Beo', power:204, acc:7.9, topSpeed:160, engine: 'Single Electric Motor', price: '$24.879', img: '/static/images/elarisBeo.png', rearImg: '/static/rearimg/elarisBeo-rear.png' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: '12 Cilindri',    name: '2025 Ferrari 12 Cilindri', power:830, acc:2.9, topSpeed:340, engine: '6.5 V12', price: '$527.000', img: '/static/images/ferrari12Cilindri.png', rearImg: '/static/rearimg/ferrari12Cilindri-rear.jpg' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: '208',            name: '1988 Ferrari 208', power:254, acc:7.0, topSpeed:242, engine: '2.0L V8 Twin-Turbo', price: '$81.900', img: '/static/images/ferrari208.png', rearImg: '/static/rearimg/ferrari208-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: '246',            name: '1972 Ferrari 246', power:196, acc:6.8, topSpeed:235, engine: '2.4L Naturally Aspirated V6', price: '$370.000', img: '/static/images/ferrari246.png', rearImg: '/static/rearimg/ferrari246-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '250',            name: '1959 Ferrari 250', power:241, acc:7.0, topSpeed:235, engine: '3.0 V12', price: '$690.000', img: '/static/images/ferrari250.png', rearImg: '/static/rearimg/ferrari250-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: '296',            name: '2025 Ferrari 296', power:880, acc:2.8, topSpeed:330, engine: '3.0 V6', price: '$293,000', img: '/static/images/ferrari296.png', rearImg: '/static/rearimg/ferrari296-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: '308',            name: '1984 Ferrari 308', power:235, acc:6.5, topSpeed:255, engine: '308 GTB Qv', price: '$98,500', img: '/static/images/ferrari308.png', rearImg: '/static/rearimg/ferrari308-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: '328',            name: '1988 Ferrari 328', power:269, acc:5.9, topSpeed:263, engine: '3.2 V8', price: '$86,900', img: '/static/images/ferrari328.png', rearImg: '/static/rearimg/ferrari328-rear.jpg' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: '330',            name: '1967 Ferrari 330', power:300, acc:6.5, topSpeed:245, engine: '4.0 V12', price: '$460,000', img: '/static/images/ferrari330.png', rearImg: '/static/rearimg/ferrari330-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: '360',            name: '2004 Ferrari 360', power:400, acc:4.6, topSpeed:290, engine: '360 Spider', price: '$95,000', img: '/static/images/ferrari360.png', rearImg: '/static/rearimg/ferrari360-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: '365',            name: '1973 Ferrari 365', power:354, acc:5.4, topSpeed:280, engine: '4.4 V12', price: '$645,000', img: '/static/images/ferrari365.png', rearImg: '/static/rearimg/ferrari365-rear.png' , consumption: { value:17.5, unit: 'L/100km' }},

  { id: '430 Scuderia',   name: '2009 Ferrari 430 Scuderia', power:510, acc:3.6, topSpeed:319, engine: '4.3L V8', price: '$299.990', img: '/static/images/ferrari430Scuderia.png', rearImg: '/static/rearimg/ferrari430Scuderia-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: '456',            name: '1999 Ferrari 456', power:442, acc:5.2, topSpeed:300, engine: 'GT 5.5 V12', price: '$70.000', img: '/static/images/ferrari456.png', rearImg: '/static/rearimg/ferrari456-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: '458',            name: '2012 Ferrari 458', power:566, acc:3.4, topSpeed:320, engine: '4.5 V8', price: '$249.980', img: '/static/images/ferrari458.png', rearImg: '/static/rearimg/ferrari458-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '488',            name: '2022 Ferrari 488', power:721, acc:2.8, topSpeed:340, engine: '3.9 V8', price: '$465.000', img: '/static/images/ferrari488.png', rearImg: '/static/rearimg/ferrari488-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: '512',            name: '1993 Ferrari 512', power:428, acc:4.8, topSpeed:314, engine: '4.9 i V12 48V', price: '$269.990', img: '/static/images/ferrari512.png', rearImg: '/static/rearimg/ferrari512-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: '550',            name: '2001 Ferrari 550', power:485, acc:4.4, topSpeed:320, engine: '5.5 V12', price: '$129.000', img: '/static/images/ferrari550.png', rearImg: '/static/rearimg/ferrari550-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: '599',            name: '2009 Ferrari 599', power:620, acc:3.7, topSpeed:330, engine: '6.0 V12', price: '$139.000', img: '/static/images/ferrari599.png', rearImg: '/static/rearimg/ferrari599-rear.jpg' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: '612',            name: '2004 Ferrari 612', power:540, acc:4.2, topSpeed:320, engine: '5.7i V12 48V', price: '$75.900', img: '/static/images/ferrari612.png', rearImg: '/static/rearimg/ferrari612-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: '812',            name: '2021 Ferrari 812', power:799, acc:3, topSpeed:340, engine: '6.5 V12', price: '$445.900', img: '/static/images/ferrari812.png', rearImg: '/static/rearimg/ferrari812-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'California',     name: '2014 Ferrari California', power:560, acc:3.6, topSpeed:315, engine: '3.9 V8', price: '$129.900', img: '/static/images/ferrariCalifornia.png', rearImg: '/static/rearimg/ferrariCalifornia-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Daytona',        name: '2025 Ferrari Daytona', power:829, acc:2.85, topSpeed:340, engine: '6.5 V12', price: '$5.300.000', img: '/static/images/ferrariDaytona.png', rearImg: '/static/rearimg/ferrariDaytona-rear.jpg' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'Dino GT4',       name: '1976 Ferrari Dino GT4', power:237, acc:6.5, topSpeed:255, engine: '308 2.9 V8', price: '$60.000', img: '/static/images/ferrariDinoGT4.png', rearImg: '/static/rearimg/ferrariDinoGT4-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Enzo Ferrari',   name: '2004 Ferrari Enzo Ferrari', power:659, acc:3.65, topSpeed:350, engine: '6.0 V12', price: '$4.890.000', img: '/static/images/ferrariEnzoFerrari.png', rearImg: '/static/rearimg/ferrariEnzoFerrari-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'F12',            name: '2016 Ferrari F12', power:741, acc:2.9, topSpeed:340, engine: '6.3 V12', price: '$254.999', img: '/static/images/ferrariF12.png', rearImg: '/static/rearimg/ferrariF12-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'F355',           name: '1999 Ferrari F355', power:379, acc:4.7, topSpeed:295, engine: '3.5 V8', price: '$129.990', img: '/static/images/ferrariF355.png', rearImg: '/static/rearimg/ferrariF355-rear.png', consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'F40',            name: '1990 Ferrari F40', power:479, acc:4.1, topSpeed:324, engine: '2.9 i V8 32V', price: '$2.450.000', img: '/static/images/ferrariF40.png', rearImg: '/static/rearimg/ferrariF40-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'F50',            name: '1996 Ferrari F50', power:521, acc:3.87, topSpeed:325, engine: '4.7 V12', price: '$5.600.000', img: '/static/images/ferrariF50.png', rearImg: '/static/rearimg/ferrariF50-rear.jpg' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'F512',           name: '1996 Ferrari F512', power:441, acc:4.7, topSpeed:315, engine: 'F512 M', price: '$490.000', img: '/static/images/ferrariF512.png', rearImg: '/static/rearimg/ferrariF512-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'F8 Spider',      name: '2022 Ferrari F8 Spider', power:721, acc:2.9, topSpeed:340, engine: '3.9 V8', price: '$350.000', img: '/static/images/ferrariF8Spider.png', rearImg: '/static/rearimg/ferrariF8Spider-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'F8 Tributo',     name: '2023 Ferrari F8 Tributo', power:721, acc:2.9, topSpeed:340, engine: '3.9 V8', price: '$304.900', img: '/static/images/ferrariF8Tributo.png', rearImg: '/static/rearimg/ferrariF8Tributo-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'F8',             name: '2023 Ferrari F8', power:721, acc:2.9, topSpeed:340, engine: '3.9 V8', price: '$304.900', img: '/static/images/ferrariF8Tributo.png', rearImg: '/static/rearimg/ferrariF8Tributo-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'FF',             name: '2012 Ferrari FF', power:661, acc:3.7, topSpeed:335, engine: '6.3 V12', price: '$124.945', img: '/static/images/ferrariFF.png', rearImg: '/static/rearimg/ferrariFF-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'GTC4 Lusso',     name: '2019 Ferrari GTC4 Lusso', power:688, acc:3.4, topSpeed:335, engine: '6.3 V12', price: '$235.000', img: '/static/images/ferrariGTC4Lusso.png', rearImg: '/static/rearimg/ferrariGTC4Lusso-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'LaFerrari',      name: '2014 Ferrari LaFerrari', power:963, acc:3.0, topSpeed:350, engine: '6.3 V12', price: '$3.699.000', img: '/static/images/ferrariLaFerrari.png', rearImg: '/static/rearimg/ferrariLaFerrari-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'Monza',          name: '2021 Ferrari Monza', power:810, acc:2.9, topSpeed:300, engine: 'SP2 6.5 V12', price: '$3.950.000', img: '/static/images/ferrariMonza.png', rearImg: '/static/rearimg/ferrariMonza-rear.png' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Portofino',      name: '2020 Ferrari Portofino', power:600, acc:3.5, topSpeed:320, engine: '3.9 V8', price: '$189.900', img: '/static/images/ferrariPortofino.png', rearImg: '/static/rearimg/ferrariPortofino-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Purosangue',     name: '2024 Ferrari Purosangue', power:725, acc:3.3, topSpeed:310, engine: '6.5 V12', price: '$529.990', img: '/static/images/ferrariPurosangue.png', rearImg: '/static/rearimg/ferrariPurosangue-rear.png' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Roma',           name: '2023 Ferrari Roma', power:620, acc:3.4, topSpeed:320, engine: '3.9 V8', price: '$220.000', img: '/static/images/ferrariRoma.png', rearImg: '/static/rearimg/ferrariRoma-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'SF90 Spider',    name: '2023 Ferrari SF90 Spider', power:999, acc:2.5, topSpeed:340, engine: '4.0 V8', price: '$510.000', img: '/static/images/ferrariSF90Spider.png', rearImg: '/static/rearimg/ferrariSF90Spider-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Superamerica',   name: '2006 Ferrari Superamerica', power:540, acc:4.2, topSpeed:320, engine: '575M Superamerica', price: '$375.000', img: '/static/images/ferrariSuperamerica.png', rearImg: '/static/rearimg/ferrariSuperamerica-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Karma',         name: '2012 Fisker Karma', power:408, acc:6.3, topSpeed:200, engine: '2.0L Turbo', price: '$32.500', img: '/static/images/fiskerKarma.png', rearImg: '/static/rearimg/fiskerKarma-rear.jpg' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Bronco',        name: '2023 Ford Bronco', power:334, acc:7.2, topSpeed:160, engine: '2.7L V6', price: '$59.980', img: '/static/images/fordBronco.png', rearImg: '/static/rearimg/fordBronco-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Mustang',       name: '2020 Ford Mustang', power:450, acc:4.8, topSpeed:249, engine: '5.0 SHELBY GT 500', price: '$37.950', img: '/static/images/fordMustang.png', rearImg: '/static/rearimg/fordMustang-rear.jpg' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'Mustang Mach-E',   name: '2023 Ford Mustang Mach-E', power:487, acc:3.8, topSpeed:200, engine: 'GT 98.7 kWh', price: '$30.990', img: '/static/images/fordMustangMachE.png', rearImg: '/static/rearimg/fordMustangMachE-rear.jpg' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'GT',            name: '2021 Ford GT', power:649, acc:2.8, topSpeed:347, engine: '3.5L V6', price: '$890.000', img: '/static/images/fordGT.jpg', rearImg: '/static/rearimg/fordGT-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'G70',           name: '2025 Genesis G70', power:245, acc:6.4, topSpeed:235, engine: '2.0 Turbo', price: '$46.990', img: '/static/images/genesisG70.png', rearImg: '/static/rearimg/genesisG70-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'G80',           name: '2022 Genesis G80', power:209, acc:7.8, topSpeed:230, engine: '2.2L Turbo', price: '$37.900', img: '/static/images/genesisG80.png', rearImg: '/static/rearimg/genesisG80-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'G90',           name: '2024 Genesis G90', power:415, acc:5.4, topSpeed:250, engine: '3.5L Twin-Turbo V6 MHEV', price: '$80.000', img: '/static/images/genesisG90.png', rearImg: '/static/rearimg/genesisG90-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'GV80',          name: '2024 Genesis GV80', power:305, acc:6.9, topSpeed:230, engine: '2.5L Turbocharged Inline-4', price: '$62.980', img: '/static/images/genesisGV80.png', rearImg: '/static/rearimg/genesisGV80-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Z',             name: '2025 Hiphi Z', power:670, acc:3.8, topSpeed:200, engine: '90.2 kWh', price: '$69.800', img: '/static/images/hiphiZ.png', rearImg: '/static/rearimg/hiphiZ-rear.jpg' , consumption: { value:21.0, unit: 'kWh/100km' }},

  { id: 'E-HS9',         name: '2024 Hongqi E-HS9', power:551, acc:4.9, topSpeed:200, engine: '99 kWh', price: '$63.999', img: '/static/images/hongqiEHS9.png', rearImg: '/static/rearimg/hongqiEHS9-rear.png' , consumption: { value:24.0, unit: 'kWh/100km' }},

  { id: 'H5',            name: '2025 Hongqi H5', power:224, acc:7.8, topSpeed:230, engine: '2.0L Turbocharged Inline-4', price: '$52.000', img: '/static/images/hongqiH5.png', rearImg: '/static/rearimg/hongqiH5-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'H2',            name: '2005 HUMMER H2', power:315, acc:10.5, topSpeed:160, engine: '6.0L V8', price: '$29.995', img: '/static/images/hummerH2.png', rearImg: '/static/rearimg/hummerH2-rear.jpg' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'i10',           name: '2025 Hyundai i10', power:90, acc:11.5, topSpeed:180, engine: '1.0L 3-Cylinder Turbocharged', price: '$22.990', img: '/static/images/hyundaii10.png', rearImg: '/static/rearimg/hyundaii10-rear.png' , consumption: { value:5.0, unit: 'L/100km' }},

  { id: 'i20',           name: '2024 Hyundai i20', power:204, acc:6.7, topSpeed:230, engine: '1.6L 4-Cylinder Turbocharged', price: '$32.990', img: '/static/images/hyundaii20.png', rearImg: '/static/rearimg/hyundaii20-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'i30',           name: '2024 Hyundai i30', power:280, acc:5.4, topSpeed:250, engine: '2.0L 4-Cylinder Turbocharged', price: '$35.995', img: '/static/images/hyundaii30.png', rearImg: '/static/rearimg/hyundaii30-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'IONIQ 5',       name: '2024 Hyundai IONIQ 5', power:170, acc:8.5, topSpeed:185, engine: 'Single Electric Motor', price: '$30.990', img: '/static/images/hyundaiIONIQ5.png', rearImg: '/static/rearimg/hyundaiIONIQ5-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Q60',           name: '2017 Infiniti Q60', power:211, acc:7.3, topSpeed:235, engine: '2.0 Turbo', price: '$25.999', img: '/static/images/infinitiQ60.png', rearImg: '/static/rearimg/infinitiQ60-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'T8',            name: '2023 JAC T8', power:204, acc:11, topSpeed:170, engine: '2.0L 4-Cylinder Turbocharged', price: '$24.950', img: '/static/images/jacT8.png', rearImg: '/static/rearimg/jacT8-rear.png' , consumption: { value:9.5, unit: 'L/100km' }},

  { id: 'XE',            name: '2022 Jaguar XE', power:300, acc:5.9, topSpeed:250, engine: '2.0i', price: '$32.900', img: '/static/images/jaguarXE.png', rearImg: '/static/rearimg/jaguarXE-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'F-Type',        name: '2024 Jaguar F-Type', power:575, acc:3.7, topSpeed:300, engine: '5.0 V8', price: '$83.480', img: '/static/images/jaguarFType.png', rearImg: '/static/rearimg/jaguarFType-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'F-Type 2',      name: '2017 Jaguar F-Type', power:575, acc:3.5, topSpeed:322, engine: 'SVR 5.0 V8', price: '$62.900', img: '/static/images/jaguarFType2.png', rearImg: '/static/rearimg/jaguarFType2-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Wrangler',      name: '2023 Jeep Wrangler', power:381, acc:6.4, topSpeed:177, engine: 'Sahara 2.0L', price: '$65.000', img: '/static/images/jeepWrangler.png', rearImg: '/static/rearimg/jeepWrangler-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Torres',        name: '2025 KGM Torres', power:163, acc:10.8, topSpeed:190, engine: '1.5 Turbo', price: '$22.990', img: '/static/images/kgmTorres.png', rearImg: '/static/rearimg/kgmTorres-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Ceed',          name: '2025 Kia Ceed', power:140, acc:9.7, topSpeed:197, engine: '	1.5 T-GDI', price: '$25.810', img: '/static/images/kiaCeed.png', rearImg: '/static/rearimg/kiaCeed-rear.png' , consumption: { value:14.0, unit: 'kWh/100km' }},

  { id: 'e-Niro',        name: '2024 Kia e-Niro', power:204, acc:7.8, topSpeed:167, engine: 'e-Niro 64.8 kWh', price: '$28.745', img: '/static/images/kiaeNiro.png', rearImg: '/static/rearimg/kiaeNiro-rear.jpg' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'EV3',           name: '2025 Kia EV3', power:204, acc:7.5, topSpeed:170, engine: '81.4 kWh', price: '$28.250', img: '/static/images/kiaEv3.png', rearImg: '/static/rearimg/kiaEv3-rear.jpg' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'EV4',           name: '2025 Kia EV4', power:204, acc:7.4, topSpeed:170, engine: '58.3 kWh', price: '$45.900', img: '/static/images/kiaEv4.png', rearImg: '/static/rearimg/kiaEv4-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'EV5',           name: '2025 Kia EV5', power:313, acc:6.1, topSpeed:185, engine: '88.1 kWh', price: '$49.980', img: '/static/images/kiaEv5.png', rearImg: '/static/rearimg/kiaEv5-rear.jpg' , consumption: { value:18.0, unit: 'kWh/100km' }},

  { id: 'EV6',           name: '2025 Kia EV6', power:609, acc:3.9, topSpeed:259, engine: 'GT 84 kWh', price: '$51.988', img: '/static/images/kiaEv6.png', rearImg: '/static/rearimg/kiaEv6-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'EV9',           name: '2024 Kia EV9', power:508, acc:4.6, topSpeed:220, engine: 'GT 99.8 kWh', price: '$67.950', img: '/static/images/kiaEv9.png', rearImg: '/static/rearimg/kiaEv9-rear.jpg' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'K4',            name: '2025 Kia K4', power:180, acc:8.4, topSpeed:206, engine: '1.6 T-GDI', price: '$35.210', img: '/static/images/kiaK4.png', rearImg: '/static/rearimg/kiaK4-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Soul',          name: '2024 Kia Soul', power:204, acc:7.9, topSpeed:167, engine: 'e-Soul 67 kWh', price: '$27.995', img: '/static/images/kiaSoul.png', rearImg: '/static/rearimg/kiaSoul-rear.png' , consumption: { value:15.0, unit: 'kWh/100km' }},

  { id: 'Sportage',      name: '2023 Kia Sportage', power:239, acc:8.1, topSpeed:196, engine: '1.6 T-GDI', price: '$21.900', img: '/static/images/kiaSportage.png', rearImg: '/static/rearimg/kiaSportage-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Stinger',       name: '2019 Kia Stinger', power:370, acc:4.9, topSpeed:270, engine: 'GT 3.3 GDI', price: '$28.990', img: '/static/images/kiaStinger.png', rearImg: '/static/rearimg/kiaStinger-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'XCeed',         name: '2025 Kia XCeed', power:101, acc:7.5, topSpeed:220, engine: '1.6 T-GDI', price: '$22.980', img: '/static/images/kiaXCeed.png', rearImg: '/static/rearimg/kiaXCeed-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Agera',        name: '2018 Koenigsegg Agera', power:960, acc:3, topSpeed:420, engine: '5.0 V8', price: '$1.800.000', img: '/static/images/koenigseggAgera.png', rearImg: '/static/rearimg/koenigseggAgera-rear.jpg' , consumption: { value:22.0, unit: 'L/100km' }},

  { id: 'Agera R',      name: '2014	Koenigsegg Agera R', power:1140, acc:2.8, topSpeed:420, engine: 'R 5.0 V8', price: '$2.200.000', img: '/static/images/koenigseggAgeraR.png', rearImg: '/static/rearimg/koenigseggAgeraR-rear.png' , consumption: { value:23.0, unit: 'L/100km' }},

  { id: 'Agera RS',     name: '2016 Koenigsegg Agera RS', power:1160, acc:2.5, topSpeed:443, engine: 'RS 5.0 V8', price: '$3.000.000', img: '/static/images/koenigseggAgeraRS.png', rearImg: '/static/rearimg/koenigseggAgeraRS-rear.png' , consumption: { value:23.0, unit: 'L/100km' }},

  { id: 'CC',           name: '2024 Koenigsegg CC', power:1385, acc:2.7, topSpeed:465, engine: '5.0 V8', price: '$3.102.500', img: '/static/images/koenigseggCC.png', rearImg: '/static/rearimg/koenigseggCC-rear.png' , consumption: { value:22.0, unit: 'L/100km' }},

  { id: 'Jesko',        name: '2024 Koenigsegg Jesko', power:1599, acc:2.5, topSpeed:480, engine: '5.0L Twin-Turbo V8', price: '$3.800.000', img: '/static/images/koenigseggJesko.png', rearImg: '/static/rearimg/koenigseggJesko-rear.jpg' , consumption: { value:25.0, unit: 'L/100km' }},

  { id: 'One:1',        name: '2015 Koenigsegg One:1', power:1360, acc:2.8, topSpeed:440, engine: '	5.0 V8', price: '$3.500.000', img: '/static/images/koenigseggOne1.png', rearImg: '/static/rearimg/koenigseggOne1-rear.png' , consumption: { value:25.0, unit: 'L/100km' }},

  { id: 'Regera',       name: '2021 Koenigsegg Regera', power:1500, acc:2.8, topSpeed:410, engine: '5.0 L V8', price: '$4.500.000', img: '/static/images/koenigseggRegera.png', rearImg: '/static/rearimg/koenigseggRegera-rear.png' , consumption: { value:22.0, unit: 'L/100km' }},

  { id: 'X-Bow GT',     name: '2025 KTM X-Bow GT', power:500, acc:3.4, topSpeed:280, engine: '2.5 TFSI', price: '$429.900', img: '/static/images/ktmXbowgt.png', rearImg: '/static/rearimg/ktmXbowgt-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'X-Bow GT4',    name: '2017 KTM X-Bow GT4', power:360, acc:3.5, topSpeed:260, engine: '2.0L Turbo', price: '$82.900', img: '/static/images/ktmXbowgt4.png', rearImg: '/static/rearimg/ktmXbowgt4-rear.webp' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'X-Bow R',      name: '2023 KTM X-Bow R', power:300, acc:3.9, topSpeed:220, engine: 'R 2.0', price: '$85.000', img: '/static/images/ktmXbowr.png', rearImg: '/static/rearimg/ktmXbowr-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'X-Bow Street',  name: '2011 KTM X-Bow Street', power:241, acc:3.9, topSpeed:220, engine: '2.0L Turbocharged', price: '$85.000', img: '/static/images/ktmXbowstreet.png', rearImg: '/static/rearimg/ktmXbowstreet-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: '400 GT',       name: '1967 Lamborghini 400 GT', power:320, acc:6.2, topSpeed:270, engine: '3.9 V12', price: '$345.000', img: '/static/images/lamborghini400gt.png', rearImg: '/static/rearimg/lamborghini400gt-rear.png' , consumption: { value:17.5, unit: 'L/100km' }},

  { id: 'Aventador',    name: '2022 Lamborghini Aventador', power:780, acc:2.9, topSpeed:355, engine: '6.5 V12', price: '$570.900', img: '/static/images/lamborghiniAventador.png', rearImg: '/static/rearimg/lamborghiniAventador-rear.jpg' , consumption: { value:18.5, unit: 'L/100km' }},

  { id: 'Asterion',     name: '2019 Lamborghini Asterion', power:910, acc:3, topSpeed:320, engine: '5.2 V10', price: '$1.200.000', img: '/static/images/lamborghiniAsterion.png', rearImg: '/static/rearimg/lamborghiniAsterion-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Centenario',   name: '2018 Lamborghini Centenario', power:770, acc:2.9, topSpeed:350, engine: '6.5 V12', price: '$2.000.000', img: '/static/images/lamborghiniCentenario.png', rearImg: '/static/rearimg/lamborghiniCentenario-rear.jpg' , consumption: { value:19.5, unit: 'L/100km' }},

  { id: 'Countach',     name: '2023 Lamborghini Countach', power:814, acc:2.8, topSpeed:355, engine: '6.5 V12', price: '$2.796.500', img: '/static/images/lamborghiniCountach.jpg', rearImg: '/static/rearimg/lamborghiniCountach-rear.jpg' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'Countach 2',   name: '1989 Lamborghini Countach', power:455, acc:5, topSpeed:295, engine: 'LP5000 QV', price: '$950.000', img: '/static/images/lamborghiniCountach2.png', rearImg: '/static/rearimg/lamborghiniCountach2-rear.jpg' , consumption: { value:18.5, unit: 'L/100km' }},

  { id: 'Diablo',       name: '1996 Lamborghini Diablo', power:492, acc:4.1, topSpeed:325, engine: 'VT', price: '$545.000', img: '/static/images/lamborghiniDiablo.png', rearImg: '/static/rearimg/lamborghiniDiablo-rear.jpg' , consumption: { value:18.5, unit: 'L/100km' }},

  { id: 'Espada',       name: '1972 Lamborghini Espada', power:349, acc:6.8, topSpeed:245, engine: '4.0L V12', price: '$125.000', img: '/static/images/lamborghiniEspada.png', rearImg: '/static/rearimg/lamborghiniEspada-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Gallardo',     name: '2014 Lamborghini Gallardo', power:551, acc:4.2, topSpeed:319, engine: '5.0 V10', price: '$144.990', img: '/static/images/lamborghiniGallardo.png', rearImg: '/static/rearimg/lamborghiniGallardo-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Huracán',      name: '2024 Lamborghini Huracán', power:639, acc:3.4, topSpeed:260, engine: '5.2 V10', price: '$375.000', img: '/static/images/lamborghiniHuracán.png', rearImg: '/static/rearimg/lamborghiniHuracán-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Huracan',      name: '2023 Lamborghini Huracan', power:610, acc:3.2, topSpeed:325, engine: '5.2 V10', price: '$249.865', img: '/static/images/lamborghiniHuracan.png', rearImg: '/static/rearimg/lamborghiniHuracan-rear.png', consumption: { value:14.1, unit: 'L/100km' }},

  { id: 'Jalpa',        name: '1985 Lamborghini Jalpa', power:250, acc:6.4, topSpeed:248, engine: 'P 350 V8', price: '$128.500', img: '/static/images/lamborghiniJalpa.png', rearImg: '/static/rearimg/lamborghiniJalpa-rear.jpg' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'LM',           name: '1987 Lamborghini LM', power:455, acc:7.8, topSpeed:210, engine: '5.2 L V12', price: '$625.000', img: '/static/images/lamborghiniLM.png', rearImg: '/static/rearimg/lamborghiniLM-rear.jpg' , consumption: { value:23.5, unit: 'L/100km' }},

  { id: 'Miura',        name: '1969 Lamborghini Miura', power:370, acc:6.7, topSpeed:300, engine: 'P400 3.9 V12', price: '$3.000.000', img: '/static/images/lamborghiniMiura.png', rearImg: '/static/rearimg/lamborghiniMiura-rear.jpg' , consumption: { value:17.5, unit: 'L/100km' }},

  { id: 'Murciélago',   name: '2007 Lamborghini Murciélago', power:640, acc:3.4, topSpeed:330, engine: '6.5 V12', price: '$369.990', img: '/static/images/lamborghiniMurciélago.jpg', rearImg: '/static/rearimg/lamborghiniMurciélago-rear.png' , consumption: { value:18.5, unit: 'L/100km' }},

  { id: 'Reventon',     name: '2009 Lamborghini Reventon', power:640, acc:3.4, topSpeed:340, engine: '6.5 V12', price: '$2.000.000', img: '/static/images/lamborghiniReventon.png', rearImg: '/static/rearimg/lamborghiniReventon-rear.png' , consumption: { value:19.5, unit: 'L/100km' }},

  { id: 'Revuelto',     name: '2024 Lamborghini Revuelto', power:824, acc:2.5, topSpeed:350, engine: '6.5 V12', price: '$620.000', img: '/static/images/lamborghiniRevuelto.png', rearImg: '/static/rearimg/lamborghiniRevuelto-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Sian FKP 37',  name: '2021 Lamborghini Sian FKP 37', power:818, acc:2.8, topSpeed:350, engine: '6.5 V12', price: '$4.199.900', img: '/static/images/lamborghiniSianFKP37.jpg', rearImg: '/static/rearimg/lamborghiniSianFKP37-rear.jpg' , consumption: { value:18.2, unit: 'L/100km' }},

  { id: 'Temerario',    name: '2025 Lamborghini Temerario', power:799, acc:2.7, topSpeed:343, engine: '4.0 V8', price: '$385.252', img: '/static/images/lamborghiniTemerario.jpg', rearImg: '/static/rearimg/lamborghiniTemerario-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Urraco P250',  name: '1970 Lamborghini Urraco P250', power:250, acc:6.9, topSpeed:241, engine: 'P250', price: '$115.000', img: '/static/images/lamborghiniUrracoP250.png', rearImg: '/static/rearimg/lamborghiniUrracoP250-rear.jpg' , consumption: { value:14.5, unit: 'L/100km' }},

  { id: 'Urus',         name: '2022 Lamborghini Urus', power:650, acc:3.6, topSpeed:305, engine: '4.0 V8', price: '$269.000', img: '/static/images/lamborghiniUrus.png', rearImg: '/static/rearimg/lamborghiniUrus-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Veneno',       name: '2014 Lamborghini Veneno', power:750, acc:2.9, topSpeed:335, engine: '6.5 V12', price: '$9.000.000', img: '/static/images/lamborghiniVeneno.jpg', rearImg: '/static/rearimg/lamborghiniVeneno-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Defender',     name: '2022 Land Rover Defender', power:300, acc:8, topSpeed:191, engine: '3.0 P300', price: '$57.999', img: '/static/images/landRoverDefender.png', rearImg: '/static/rearimg/landRoverDefender-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Discovery',    name: '2021 Land Rover Discovery', power:290, acc:7.0, topSpeed:233, engine: '2.0 P290', price: '$27.990', img: '/static/images/landRoverDiscovery.png', rearImg: '/static/rearimg/landRoverDiscovery-rear.jpg' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Range Rover',   name: '2020 Land Rover Range Rover', power:400, acc:5.5, topSpeed:250, engine: '3.0 P400', price: '$76.980', img: '/static/images/landRoverRangeRover.png', rearImg: '/static/rearimg/landRoverRangeRover-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Range Rover Sport', name: '2024 Land Rover Range Rover Sport', power:355, acc:5.7, topSpeed:243, engine: 'P360 3.0', price: '$83.600', img: '/static/images/landRoverRangeRover.png', rearImg: '/static/rearimg/landRoverRangeRover-rear.png' , consumption: { value:10.7, unit: 'L/100km' }},

  { id: 'Range Rover Evoque',   name: '2024 Land Rover Range Rover Evoque', power:249, acc:7.6, topSpeed:230, engine: '2.0 P250', price: '$44.450', img: '/static/images/landRoverRangeRoverEvoque.png', rearImg: '/static/rearimg/landRoverRangeRoverEvoque-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Range Rover Velar',    name: '2024 Land Rover Range Rover Velar', power:204, acc:8.3, topSpeed:210, engine: '2.0 D200', price: '$59.900', img: '/static/images/landRoverRangeRoverVelar.png', rearImg: '/static/rearimg/landRoverRangeRoverVelar-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'B10',         name: '2025 Leapmotor B10', power:218, acc:6.8, topSpeed:170, engine: '67.1 kWh', price: '$29.490', img: '/static/images/leapmotorB10.png', rearImg: '/static/rearimg/leapmotorB10-rear.jpg' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'C10',         name: '2024 Leapmotor C10', power:95, acc:12.7, topSpeed:170, engine: '37.3 kWh', price: '$16.890', img: '/static/images/leapmotorC10.png', rearImg: '/static/rearimg/leapmotorC10-rear.png' , consumption: { value:18.0, unit: 'kWh/100km' }},

  { id: 'TX',          name: '2025 LEVC TX', power:150, acc:13.2, topSpeed:129, engine: '1.5 Range Extender', price: '$81.754', img: '/static/images/levcTX.png', rearImg: '/static/rearimg/levcTX-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'CT 200h',     name: '2019 Lexus CT 200h', power:136, acc:10.3, topSpeed:180, engine: '200h', price: '$17.182', img: '/static/images/lexusCT200h.png', rearImg: '/static/rearimg/lexusCT200h-rear.png' , consumption: { value:14.5, unit: 'kWh/100km' }},

  { id: 'ES 300',      name: '2024 Lexus ES 300', power:218, acc:8.9, topSpeed:180, engine: '300h', price: '$37.900', img: '/static/images/lexusES300.png', rearImg: '/static/rearimg/lexusES300-rear.png' , consumption: { value:15.0, unit: 'kWh/100km' }},

  { id: 'ES 350',      name: '2023 Lexus ES 350', power:220, acc:7.8, topSpeed:210, engine: '300h', price: '$26.719', img: '/static/images/lexusES350.png', rearImg: '/static/rearimg/lexusES350-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'GX 470',      name: '2024 Lexus GX 470', power:349, acc:6.5, topSpeed:180, engine: '3.4L V6', price: '$110.000', img: '/static/images/lexusGX470.png', rearImg: '/static/rearimg/lexusGX470-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'IS 300',      name: '2014 Lexus IS 300', power:223, acc:6.8, topSpeed:211, engine: '300 V6', price: '$22.900', img: '/static/images/lexusIS300.png', rearImg: '/static/rearimg/lexusIS300-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'LBX',         name: '2024 Lexus LBX', power:136, acc:9.6, topSpeed:170, engine: '1.5', price: '$31.990', img: '/static/images/lexusLBX.png', rearImg: '/static/rearimg/lexusLBX-rear.jpg' , consumption: { value:15.0, unit: 'kWh/100km' }},

  { id: 'LC 500',      name: '2021 Lexus LC 500', power:477, acc:4.7, topSpeed:270, engine: '500 V8', price: '$99.900', img: '/static/images/lexusLC500.png', consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'LC 500h',     name: '2018 Lexus LC 500h', power:359, acc:5.0, topSpeed:250, engine: '500h V6', price: '$77.900', img: '/static/images/lexusLC500h.png', rearImg: '/static/rearimg/lexusLC500h-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'LFA',         name: '2012 Lexus LFA', power:560, acc:3.7, topSpeed:325, engine: '4.8 V10', price: '$1.000.000', img: '/static/images/lexusLFA.png', rearImg: '/static/rearimg/lexusLFA-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'LS 500',      name: '2023 Lexus LS 500', power:359, acc:5.5, topSpeed:250, engine: '500h V6', price: '$98.495', img: '/static/images/lexusLS500.png', rearImg: '/static/rearimg/lexusLS500-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'LX 450d',     name: '2017 Lexus LX 450d', power:290, acc:8.6, topSpeed:210, engine: '450d V8', price: '$68.500', img: '/static/images/lexusLX450d.png', rearImg: '/static/rearimg/lexusLX450d-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'LX 570',      name: '2021 Lexus LX 570', power:383, acc:7.7, topSpeed:220, engine: '570 V8', price: '$99.900', img: '/static/images/lexusLX570.png', rearImg: '/static/rearimg/lexusLX570-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'LX 600',      name: '2025 Lexus LX 600', power:415, acc:6.7, topSpeed:185, engine: '3.5L V6 Twin-Turbo', price: '$185.900', img: '/static/images/lexusLX600.png', rearImg: '/static/rearimg/lexusLX600-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'LX 700h',     name: '2025 Lexus LX 700h', power:457, acc:6.8, topSpeed:210, engine: '700h V6', price: '$157.288', img: '/static/images/lexusLX700h.png', rearImg: '/static/rearimg/lexusLX700h-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},


  { id: 'NX',          name: '2024 Lexus NX', power:245, acc:7.2, topSpeed:200, engine: '350 2.4 Turbo', price: '$43.900', img: '/static/images/lexusNX300.png', rearImg: '/static/rearimg/lexusNX300-rear.png', consumption: { value:8.7, unit: 'L/100km' }},

  { id: 'NX 200t',     name: '2024 Lexus NX 200t', power:245, acc:7.1, topSpeed:200, engine: '200t', price: '$46.455', img: '/static/images/lexusNX200t.png', rearImg: '/static/rearimg/lexusNX200t-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'NX 300',      name: '2024 Lexus NX 300', power:245, acc:7.2, topSpeed:200, engine: '300', price: '$45.000', img: '/static/images/lexusNX300.png', rearImg: '/static/rearimg/lexusNX300-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'NX 300h',     name: '2018 Lexus NX 300h', power:197, acc:9.4, topSpeed:180, engine: '300h', price: '$28.600', img: '/static/images/lexusNX300h.png', rearImg: '/static/rearimg/lexusNX300h-rear.png' , consumption: { value:15.0, unit: 'kWh/100km' }},

  { id: 'NX 350h',     name: '2022 Lexus NX 350h', power:243, acc:7.7, topSpeed:200, engine: '350h', price: '$43.990', img: '/static/images/lexusNX350h.png', rearImg: '/static/rearimg/lexusNX350h-rear.png' , consumption: { value:14.5, unit: 'kWh/100km' }},

  { id: 'NX 450h+',    name: '2022 Lexus NX 450h+', power:188, acc:6.3, topSpeed:200, engine: '450h+', price: '$46.999', img: '/static/images/lexusNX450h.png', rearImg: '/static/rearimg/lexusNX450h-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'RC 200t',     name: '2016 Lexus RC 200t', power:245, acc:7.5, topSpeed:230, engine: '200t VVT-i', price: '$30.990', img: '/static/images/lexusRC200t.png', rearImg: '/static/rearimg/lexusRC200t-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'RC 300h',     name: '2019 Lexus RC 300h', power:223, acc:8.6, topSpeed:190, engine: '2.5 F Sport', price: '$39.990', img: '/static/images/lexusRC300h.png', rearImg: '/static/rearimg/lexusRC300h-rear.png' , consumption: { value:13.5, unit: 'kWh/100km' }},

  { id: 'RC F',        name: '2022 Lexus RC F', power:464, acc:4.5, topSpeed:270, engine: '5.0L V8', price: '$67.000', img: '/static/images/lexusRCF.png', rearImg: '/static/rearimg/lexusRCF-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'RX 350h',     name: '2025 Lexus RX 350', power:250, acc:7.9, topSpeed:180, engine: '350h', price: '$69.895', img: '/static/images/lexusRX350h.jpg', rearImg: '/static/rearimg/lexusRX350h-rear.png' , consumption: { value:15.5, unit: 'kWh/100km' }},

  { id: 'RX',          name: '2025 Lexus RX', power:275, acc:7.4, topSpeed:200, engine: '350 2.4 Turbo', price: '$58.875', img: '/static/images/lexusRX350h.jpg', rearImg: '/static/rearimg/lexusRX350h-rear.png', consumption: { value:8.9, unit: 'L/100km' }},

  { id: 'UX 300e',     name: '2022 Lexus UX 300e', power:204, acc:7.5, topSpeed:160, engine: '300e 72.8 kWh', price: '$24.900', img: '/static/images/lexusUX300e.png', rearImg: '/static/rearimg/lexusUX300e-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'L6',          name: '2024 Li L6', power:408, acc:5.4, topSpeed:180, engine: '1.5T 36.8 kWh', price: '$55.488', img: '/static/images/LiL6.png', rearImg: '/static/rearimg/LiL6-rear.png' , consumption: { value:14.5, unit: 'kWh/100km' }},

  { id: 'JS 50',       name: '2025 Ligier JS 50', power:8, acc:0, topSpeed:75, engine: 'L7e 12.42 kWh', price: '$25.490', img: '/static/images/ligierJS50.png', rearImg: '/static/rearimg/ligierJS50-rear.png' , consumption: { value:10.0, unit: 'kWh/100km' }},

  { id: 'MKZ',         name: '2017 Lincoln MKZ', power:241, acc:6.5, topSpeed:240, engine: '2.0L EcoBoost', price: '$50.800', img: '/static/images/lincolnMKZ.png', rearImg: '/static/rearimg/lincolnMKZ-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Nautilus',    name: '2024 Lincoln Nautilus', power:250, acc:6.8, topSpeed:210, engine: '2.0L EcoBoost', price: '$87.400', img: '/static/images/lincolnNautilus.png', rearImg: '/static/rearimg/lincolnNautilus-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Navigator',   name: '2025 Lincoln Navigator', power:441, acc:6.0, topSpeed:210, engine: '3.5L V6 EcoBoost', price: '$160.325', img: '/static/images/lincolnNavigator.png', rearImg: '/static/rearimg/lincolnNavigator-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: '2-Eleven',    name: '2008 Lotus 2-Eleven', power:300, acc:4, topSpeed:241, engine: '1.8', price: '$60.000', img: '/static/images/lotus2Eleven.png', rearImg: '/static/rearimg/lotus2Eleven-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: '3-Eleven',    name: '2018 Lotus 3-Eleven', power:436, acc:3.2, topSpeed:290, engine: '430 3.5 V6', price: '$142.000', img: '/static/images/lotus3Eleven.png', rearImg: '/static/rearimg/lotus3Eleven-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '340 R',       name: '2000 Lotus 340 R', power:190, acc:4.6, topSpeed:210, engine: '1.8 i 16V', price: '$79.890', img: '/static/images/lotus340R.png', rearImg: '/static/rearimg/lotus340R-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'Eletre',      name: '2025 Lotus Eletre', power:905, acc:2.95, topSpeed:265, engine: 'R 112 kWh', price: '$99.990', img: '/static/images/lotusEletre.png', rearImg: '/static/rearimg/lotusEletre-rear.jpg' , consumption: { value:22.0, unit: 'kWh/100km' }},

  { id: 'Elise',       name: '2018 Lotus Elise', power:220, acc:4.6, topSpeed:234, engine: '1.8', price: '$59.888', img: '/static/images/lotusElise.png', rearImg: '/static/rearimg/lotusElise-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Emeya',       name: '2025 Lotus Emeya', power:612, acc:4.2, topSpeed:250, engine: 'S 102 kWh', price: '$107.900', img: '/static/images/lotusEmeya.png', rearImg: '/static/rearimg/lotusEmeya-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'Emira',       name: '2025 Lotus Emira', power:405, acc:4.2, topSpeed:290, engine: '3.5 V6', price: '$105.000', img: '/static/images/lotusEmira.png', rearImg: '/static/rearimg/lotusEmira-rear.jpg' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'Esprit',      name: '1998 Lotus Esprit', power:354, acc:4.9, topSpeed:282, engine: '3.5 i V8 32V Turbo', price: '$60.500', img: '/static/images/lotusEsprit.png', rearImg: '/static/rearimg/lotusEsprit-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Europa',      name: '2009 Lotus Europa', power:203, acc:5.8, topSpeed:230, engine: '2.0 16V', price: '$55.000', img: '/static/images/lotusEuropa.png', rearImg: '/static/rearimg/lotusEuropa-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Evora',       name: '2019 Lotus Evora', power:411, acc:4.2, topSpeed:298, engine: '3.5 V6', price: '$97.195', img: '/static/images/lotusEvora.png', rearImg: '/static/rearimg/lotusEvora-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Exige',       name: '2009 Lotus Exige', power:246, acc:3.9, topSpeed:249, engine: '1.8 i 16V Sport 240R', price: '$53.990', img: '/static/images/lotusExige.png', rearImg: '/static/rearimg/lotusExige-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Omega',       name: '1992 Lotus Omega', power:377, acc:5.4, topSpeed:282, engine: '3.6 24V Lotus CAT', price: '$108.500', img: '/static/images/lotusOmega.png', rearImg: '/static/rearimg/lotusOmega-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},
  
  { id: 'Air',         name: '2024 Lucid Air', power:1.126, acc:2.7, topSpeed:270, engine: 'Dream Edition Performance 118 kWh', price: '$150.513', img: '/static/images/lucidAir.png', rearImg: '/static/rearimg/lucidAir-rear.png' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'Co 01',       name: '2023 Lynk & Co 01', power:261, acc:7.3, topSpeed:210, engine: '1.5L Turbo', price: '$23.800', img: '/static/images/lynkCo01.png', rearImg: '/static/rearimg/lynkCo01-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Co 02',       name: '2025 Lynk & Co 02', power:272, acc:5.5, topSpeed:180, engine: 'Electric Motor', price: '$33.490', img: '/static/images/lynkCo02.png', rearImg: '/static/rearimg/lynkCo02-rear.jpg' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'Co 08',       name: '2025 Lynk & Co 08', power:544, acc:4.6, topSpeed:190, engine: '1.5L Turbo', price: '$48.900', img: '/static/images/lynkCo08.png', rearImg: '/static/rearimg/lynkCo08-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: '3200',        name: '1999 Maserati 3200', power:368, acc:5.1, topSpeed:280, engine: '3.2 Biturbo V8 32V', price: '$25.900', img: '/static/images/maserati3200.png', rearImg: '/static/rearimg/maserati3200-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Bora',        name: '1975 Maserati Bora', power:310, acc:6.5, topSpeed:280, engine: '4.7 V8', price: '$199.000', img: '/static/images/maseratiBora.png', rearImg: '/static/rearimg/maseratiBora-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Ghibli',      name: '2023 Maserati Ghibli', power:430, acc:4.7, topSpeed:286, engine: 'S Q4 3.0 V6', price: '$67.650', img: '/static/images/maseratiGhibli.png', rearImg: '/static/rearimg/maseratiGhibli-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'GranCabrio',  name: '2025 Maserati GranCabrio', power:549, acc:3.6, topSpeed:316, engine: 'Trofeo 3.0 V6', price: '$183.900', img: '/static/images/maseratiGranCabrio.png', rearImg: '/static/rearimg/maseratiGranCabrio-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'GranTurismo',   name: '2017 Maserati GranTurismo', power:460, acc:4.8, topSpeed:299, engine: 'Sport 4.7 V8', price: '$99.000', img: '/static/images/maseratiGranTurismo.png', rearImg: '/static/rearimg/maseratiGranTurismo-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Grecale',     name: '2025 Maserati Grecale', power:300, acc:5.6, topSpeed:240, engine: 'GT 2.0', price: '$61.990', img: '/static/images/maseratiGrecale.png', rearImg: '/static/rearimg/maseratiGrecale-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'GT2 Stradale',   name: '2025 Maserati GT2 Stradale', power:639, acc:2.8, topSpeed:324, engine: '3.0 V6', price: '$395.000', img: '/static/images/maseratiGT2Stradale.png', rearImg: '/static/rearimg/maseratiGT2Stradale-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Indy',        name: '1970 Maserati Indy', power:208, acc:7.0, topSpeed:235, engine: '4.2 L V8', price: '$69.900', img: '/static/images/maseratiIndy.png', rearImg: '/static/rearimg/maseratiIndy-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Levante',     name: '2020 Maserati Levante', power:430, acc:5.2, topSpeed:264, engine: 'S 3.0 V6 GDI', price: '$50.998', img: '/static/images/maseratiLevante.png', rearImg: '/static/rearimg/maseratiLevante-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'MC12',        name: '2005 Maserati MC12', power:631, acc:3.8, topSpeed:330, engine: '6.0 V12', price: '$3.500.000', img: '/static/images/maseratiMC12.png', rearImg: '/static/rearimg/maseratiMC12-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'MC20',        name: '2023 Maserati MC20', power:630, acc:3, topSpeed:320, engine: '3.0 V6 Twin Turbo', price: '$219.000', img: '/static/images/maseratiMC20.png', rearImg: '/static/rearimg/maseratiMC20-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Merak',       name: '1988 Maserati Merak', power:159, acc:8.0, topSpeed:230, engine: '3.0 L V6', price: '$60.000', img: '/static/images/maseratiMerak.png', rearImg: '/static/rearimg/maseratiMerak-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},
  
  { id: 'Racing',      name: '1991 Maserati Racing', power:283, acc:5.9, topSpeed:255, engine: '2.0 L V6 Biturbo', price: '$39.990', img: '/static/images/maseratiRacing.png', rearImg: '/static/rearimg/maseratiRacing-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},
  
  { id: 'eTERRON 9',   name: '2025 Maxus eTERRON 9', power:442, acc:5, topSpeed:190, engine: '102.2 kWh', price: '$79.255', img: '/static/images/maxusETERRON9.png', rearImg: '/static/rearimg/maxusETERRON9-rear.png' , consumption: { value:24.5, unit: 'kWh/100km' }},

  { id: 'Euniq 6',     name: '2024 Maxus Euniq 6', power:245, acc:8.9, topSpeed:180, engine: '1.3TI', price: '$29.490', img: '/static/images/maxusEuniq6.png', rearImg: '/static/rearimg/maxusEuniq6-rear.png' , consumption: { value:21.5, unit: 'kWh/100km' }},

  { id: '57',          name: '2008 Maybach 57', power:612, acc:5, topSpeed:275, engine: '6.0 V12', price: '$119.995', img: '/static/images/maybach57.png', rearImg: '/static/rearimg/maybach57-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: '62',          name: '2011 Maybach 62', power:551, acc:5.1, topSpeed:275, engine: '6.0 V12', price: '$239.990', img: '/static/images/maybach62.jpg', rearImg: '/static/rearimg/maybach62-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'CX-80',       name: '2024 Mazda CX-80', power:192, acc:8.4, topSpeed:219, engine: '3.3 e-Skyactiv D', price: '$54.950', img: '/static/images/mazdaCX80.jpg', rearImg: '/static/rearimg/mazdaCX80-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'RX-7',        name: '1993 Mazda RX-7', power:239, acc:5.3, topSpeed:250, engine: 'Wankel Twin Turbo', price: '$65.000', img: '/static/images/mazdaRX7.jpg', rearImg: '/static/rearimg/mazdaRX7-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},
  
  { id: '12 C',        name: '2012 McLaren 12 C', power:600, acc:3.3, topSpeed:329, engine: '3.8 V8', price: '$130.000', img: '/static/images/mclaren12C.png', rearImg: '/static/rearimg/mclaren12C-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '540C',        name: '2018 McLaren 540C', power:540, acc:3.5, topSpeed:320, engine: '3.8 V8', price: '$144.990', img: '/static/images/mclaren540C.png', rearImg: '/static/rearimg/mclaren540C-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: '570GT',       name: '2019 McLaren 570GT', power:570, acc:3.4, topSpeed:328, engine: '3.8 L V8 Bi-Turbo', price: '$149.570', img: '/static/images/mclaren570GT.png', rearImg: '/static/rearimg/mclaren570GT-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: '570S',        name: '2016 McLaren 570S', power:570, acc:3.2, topSpeed:328, engine: '3.8 V8', price: '$149.990', img: '/static/images/mclaren570S.png', rearImg: '/static/rearimg/mclaren570S-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: '600LT',       name: '2019 McLaren 600LT', power:600, acc:2.9, topSpeed:324, engine: '3.8 V8', price: '$229.990', img: '/static/images/mclaren600LT.png', rearImg: '/static/rearimg/mclaren600LT-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '620R',        name: '2020 McLaren 620R', power:620, acc:2.9, topSpeed:322, engine: '3.8 V8', price: '$274.950', img: '/static/images/mclaren620R.png', rearImg: '/static/rearimg/mclaren620R-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '650S Coupe',  name: '2018 McLaren 650S Coupe', power:650, acc:3, topSpeed:333, engine: '3.8 V8', price: '$210.000', img: '/static/images/mclaren650SCoupe.png', rearImg: '/static/rearimg/mclaren650SCoupe-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '650S Spider', name: '2014 McLaren 650S Spider', power:650, acc:3, topSpeed:329, engine: '3.8 V8', price: '$162.500', img: '/static/images/mclaren650SSpider.png', rearImg: '/static/rearimg/mclaren650SSpider-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '675LT',       name: '2017 McLaren 675LT', power:675, acc:2.9, topSpeed:326, engine: '3.8 V8', price: '$309.980', img: '/static/images/mclaren675LT.webp', rearImg: '/static/rearimg/mclaren675LT-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '720S',        name: '2018 McLaren 720S', power:806, acc:2.9, topSpeed:341, engine: '4.0 V8', price: '$219.995', img: '/static/images/mclaren720S.jpg', rearImg: '/static/rearimg/mclaren720S-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '750S',        name: '2023 McLaren 750S', power:750, acc:2.8, topSpeed:332, engine: '4.0 V8', price: '$335.000', img: '/static/images/mclaren750S.png', rearImg: '/static/rearimg/mclaren750S-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: '765LT Coupe',  name: '2021 McLaren 765LT Coupe', power:765, acc:2.8, topSpeed:330, engine: '4.0 V8', price: '$489.670', img: '/static/images/mclaren765LTCoupe.png', rearImg: '/static/rearimg/mclaren765LTCoupe-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '765LT Spider', name: '2022 McLaren 765LT Spider', power:765, acc:2.8, topSpeed:330, engine: '4.0 V8', price: '$487.900', img: '/static/images/mcLaren765LTSpider.jpg', rearImg: '/static/rearimg/mcLaren765LTSpider-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Artura',       name: '2023 McLaren Artura', power:700, acc:3.0, topSpeed:330, engine: '3.0 V6', price: '$218.900', img: '/static/images/mclarenArtura.jpg', rearImg: '/static/rearimg/mclarenArtura-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'Elva',         name: '2022 McLaren Elva', power:814, acc:2.8, topSpeed:326, engine: '4.0 L Twin-Turbo V8', price: '$1.550.000', img: '/static/images/mclarenElva.png', rearImg: '/static/rearimg/mclarenElva-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'F1',           name: '2000 McLaren F1', power:627, acc:3.5, topSpeed:386, engine: '6.1 V12', price: '$17.000.000', img: '/static/images/mcLarenF1.jpg', rearImg: '/static/rearimg/mcLarenF1-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'GT 2',          name: '2021 McLaren GT', power:620, acc:3.1, topSpeed:326, engine: '4.0 V8', price: '$154.740', img: '/static/images/mcLarenGT.png', rearImg: '/static/rearimg/mcLarenGT-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'GTS',          name: '2025 McLaren GTS', power:634, acc:3.2, topSpeed:326, engine: '4.0 V8', price: '$270.000', img: '/static/images/mcLarenGTS.png', rearImg: '/static/rearimg/mcLarenGTS-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'MP4-12C',      name: '2013 McLaren MP4-12C', power:625, acc:3.3, topSpeed:329, engine: '3.8 V8', price: '$139.990', img: '/static/images/mcLarenmp4-12c.png', rearImg: '/static/rearimg/mcLarenmp4-12c-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'P1',           name: '2016 McLaren P1', power:916, acc:2.8, topSpeed:350, engine: 'P1 V8', price: '$2.399.900', img: '/static/images/mcLarenP1.jpg', rearImg: '/static/rearimg/mcLarenP1-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Senna',        name: '2018 McLaren Senna', power:800, acc:2.8, topSpeed:335, engine: '4.0 V8', price: '$1.300.780', img: '/static/images/mcLarenSenna.png', rearImg: '/static/rearimg/mcLarenSenna-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'Speedtail',    name: '2021 McLaren Speedtail', power:1070, acc:3.0, topSpeed:403, engine: '4.0 V8', price: '$2.880.000', img: '/static/images/mcLarenSpeedtail.png', rearImg: '/static/rearimg/mcLarenSpeedtail-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Cyberster',    name: '2025 MG Cyberster', power:340, acc:3.2, topSpeed:200, engine: '77 kWh', price: '$59.990', img: '/static/images/mgCyberster.png', rearImg: '/static/rearimg/mgCyberster-rear.jpg' , consumption: { value:17.5, unit: 'kWh/100km' }},

  { id: 'MG4',          name: 'MG MG4', power:245, acc:6.5, topSpeed:180, engine: '77 kWh', price: '$21.900', img: '/static/images/mgMG4.png', rearImg: '/static/rearimg/mgMG4-rear.jpg' , consumption: { value:16.5, unit: 'kWh/100km' }},

  { id: 'MGS5 EV',      name: '2025 MG MGS5 EV', power:114, acc:6.3, topSpeed:163, engine: '64 kWh', price: '$34.900', img: '/static/images/mgMGS5EV.jpg', rearImg: '/static/rearimg/mgMGS5EV-rear.png' , consumption: { value:18.0, unit: 'kWh/100km' }},

  { id: 'Cooper C',     name: '2025 MINI Cooper C', power:156, acc:8, topSpeed:225, engine: 'Cooper C 1.5', price: '$26.195', img: '/static/images/miniCooperC.png', rearImg: '/static/rearimg/miniCooperC-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},
  
  { id: 'Cooper E',     name: '2025 MINI Cooper E', power:184, acc:7.3, topSpeed:160, engine: 'Cooper E 40.7 kWh', price: '$29.408', img: '/static/images/miniCooperE.png', rearImg: '/static/rearimg/miniCooperE-rear.png' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'John Cooper Works',  name: '2022 MINI John Cooper Works', power:231, acc:6.1, topSpeed:246, engine: '2.0 L TwinPower Turbo', price: '$28.400', img: '/static/images/miniJohnCooperWorks.jpg', rearImg: '/static/rearimg/miniJohnCooperWorks-rear.png' , consumption: { value:15.5, unit: 'kWh/100km' }},

  { id: 'Aceman',       name: '2025 MINI Aceman', power:184, acc:7.9, topSpeed:160, engine: 'E 38.5 kWh', price: '$34.900', img: '/static/images/miniAceman.png', rearImg: '/static/rearimg/miniAceman-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'Cooper S Cabrio',  name: '2022 MINI Cooper S Cabrio', power:178, acc:6.9, topSpeed:230, engine: 'Cooper S 2.0', price: '$28.850', img: '/static/images/miniCooperSCabrio.png', rearImg: '/static/rearimg/miniCooperSCabrio-rear.png' , consumption: { value:14.0, unit: 'kWh/100km' }},

  { id: 'M.Go',         name: '2025 Microcar M.Go', power:8, acc:0, topSpeed:45, engine: '6 kW', price: '$19.039', img: '/static/images/microcarM.Go.png', rearImg: '/static/rearimg/microcarM.Go-rear.png' , consumption: { value:10.0, unit: 'kWh/100km' }},

  { id: 'Ferox',        name: '2025 Militem Ferox', power:470, acc:4.8, topSpeed:180, engine: '6.4L V8', price: '$210.000', img: '/static/images/militemFerox.png', rearImg: '/static/rearimg/militemFerox-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'Magnum',       name: '2022 Militem Magnum', power:401, acc:5.5, topSpeed:200, engine: '5.7L V8', price: '$95.000', img: '/static/images/militemMagnum.png', rearImg: '/static/rearimg/militemMagnum-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Grandis',      name: '2025 Mitsubishi Grandis', power:141, acc:9.4, topSpeed:180, engine: '1.3', price: '$32.990', img: '/static/images/mitsubishiGrandis.png', rearImg: '/static/rearimg/mitsubishiGrandis-rear.png' , consumption: { value:8.5, unit: 'L/100km' }},

  { id: 'L200',         name: '2021 Mitsubishi L200', power:201, acc:13, topSpeed:170, engine: '2.4 MIVEC', price: '$26.990', img: '/static/images/mitsubishiL200.png', rearImg: '/static/rearimg/mitsubishiL200-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'Lancer',       name: '2000 Mitsubishi Lancer', power:280, acc:4.9, topSpeed:250, engine: '2.0 4WD', price: '$79.990', img: '/static/images/mitsubishiLancer.png', rearImg: '/static/rearimg/mitsubishiLancer-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Lancer Evo',   name: '2006 Mitsubishi Lancer Evo', power:280, acc:5.2, topSpeed:255, engine: '2.0 MIVEC', price: '$53.000', img: '/static/images/mitsubishiLancerEvo.png', rearImg: '/static/rearimg/mitsubishiLancerEvo-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},
  
  { id: 'Plus Six',     name: '2020 Morgan Plus Six', power:340, acc:4.2, topSpeed:267, engine: '3.0 TwinPower Turbo', price: '$117.500', img: '/static/images/morganPlusSix.png', rearImg: '/static/rearimg/morganPlusSix-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'Supersport',   name: '2025 Morgan Supersport', power:340, acc:4.3, topSpeed:240, engine: '3.0L TwinPower', price: '$165.260', img: '/static/images/morganSupersport.png', rearImg: '/static/rearimg/morganSupersport-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Aero 8',       name: '2013 Morgan Aero 8', power:286, acc:5, topSpeed:257, engine: '4.4 i V8 32V', price: '$109.650', img: '/static/images/morganAero8.png', rearImg: '/static/rearimg/morganAero8-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'EL6',          name: '2025 NIO EL6', power:489, acc:4.3, topSpeed:200, engine: 'Dual Electric Motor', price: '$75.000', img: '/static/images/NIOEL6.png', rearImg: '/static/rearimg/NIOEL6-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'EL7',          name: 'NIO EL7', power:653, acc:3.9, topSpeed:200, engine: '480 kW', price: '$52.999', img: '/static/images/NIOEL7.png', rearImg: '/static/rearimg/NIOEL7-rear.webp' , consumption: { value:18.5, unit: 'kWh/100km' }},

  { id: '350Z',         name: '2005 Nissan 350Z', power:280, acc:6.1, topSpeed:250, engine: '3.5i V6 24V', price: '$22.500', img: '/static/images/nissan350Z.jpg', rearImg: '/static/rearimg/nissan350Z-rear.jpg' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: '370Z',         name: '2017 Nissan 370Z', power:328, acc:5.8, topSpeed:250, engine: '3.7 V6', price: '$31.999', img: '/static/images/nissan370Z.jpg', rearImg: '/static/rearimg/nissan370Z-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Ariya',        name: '2023 Nissan Ariya', power:306, acc:5.7, topSpeed:200, engine: '90 kWh', price: '$45.000', img: '/static/images/nissanAriya.png', rearImg: '/static/rearimg/nissanAriya-rear.png' , consumption: { value:18.0, unit: 'kwh/100km' }},

  { id: 'GT-R',         name: '2013 Nissan GT-R', power:600, acc:2.8, topSpeed:315, engine: 'Nismo 3.8 V6', price: '$110.990', img: '/static/images/nissanGT-R.jpg', rearImg: '/static/rearimg/nissanGT-R-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Nissan Z',     name: '2024 Nissan Z', power:400, acc:4.5, topSpeed:250, engine: '3.0 Twin-Turbo V6', price: '$44.110', consumption: { value:10.5, unit: 'L/100km' }},

  { id: 'Silvia',       name: '1997 Nissan Silvia', power:203, acc:7.3, topSpeed:235, engine: '2.0 i 16V Turbo', price: '$36.000', img: '/static/images/nissanSilvia.jpg', rearImg: '/static/rearimg/nissanSilvia-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Skyline',      name: '1999 Nissan Skyline', power:280, acc:5.3, topSpeed:250, engine: '2.6 i 24V Turbo 4WD', price: '$180.000', img: '/static/images/nissanSkyline.jpg', rearImg: '/static/rearimg/nissanSkyline-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Grandland',    name: '2022 Opel Grandland', power:300, acc:6.1, topSpeed:235, engine: 'GSe 1.6i Turbo', price: '$22.900', img: '/static/images/opelGrandland.png', rearImg: '/static/rearimg/opelGrandland-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Huayra',       name: '2017 Pagani Huayra', power:764, acc:3.0, topSpeed:360, engine: '6.0 V12', price: '$4.890.000', img: '/static/images/paganiHuayra.jpg', rearImg: '/static/rearimg/paganiHuayra-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Zonda',        name: 'Pagani Zonda', power:800, acc:2.6, topSpeed:350, engine: '6.0L V12', price: '$2.700.000', img: '/static/images/paganiZonda.jpg', rearImg: '/static/rearimg/paganiZonda-rear.jpg' , consumption: { value:20, unit: 'kWh/100km' }},

  { id: '2008',         name: '2024 Peugeot 2008', power:136, acc:8.3, topSpeed:206, engine: '1.2', price: '$20.450', img: '/static/images/peugeot2008.png', rearImg: '/static/rearimg/peugeot2008-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: '5008',         name: '2022 Peugeot 5008', power:131, acc:8.3, topSpeed:219, engine: '1.6 PureTech', price: '$21.990', img: '/static/images/peugeot5008.png', rearImg: '/static/rearimg/peugeot5008-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: '508',          name: '2024 Peugeot 508', power:131, acc:5.2, topSpeed:250, engine: 'PSE 1.6 PureTech', price: '$26.990', img: '/static/images/peugeot508.png', rearImg: '/static/rearimg/peugeot508-rear.png' , consumption: { value:15.0, unit: 'kWh/100km' }},

  { id: 'Speedster II', name: '2005 PGO Speedster II', power:190, acc:7.5, topSpeed:190, engine: '1.6L', price: '$35.000', img: '/static/images/pgoSpeedsterII.png', rearImg: '/static/rearimg/pgoSpeedsterII-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Barracuda',    name: '1969 Plymouth Barracuda', power:204, acc:8.0, topSpeed:190, engine: '5.2L V8', price: '$49.900', img: '/static/images/plymouthBarracuda.png', rearImg: '/static/rearimg/plymouthBarracuda-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'GTX',          name: '1968 Plymouth GTX', power:375, acc:6.0, topSpeed:220, engine: '7.0L V8', price: '$53.000', img: '/static/images/plymouthGTX.png', rearImg: '/static/rearimg/plymouthGTX-rear.png' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Road Runner',  name: '1970 Plymouth Road Runner', power:426, acc:5.3, topSpeed:220, engine: '7.2L V8', price: '$50.000', img: '/static/images/plymouthRoadRunner.png', rearImg: '/static/rearimg/plymouthRoadRunner-rear.png' , consumption: { value:21.0, unit: 'L/100km' }},

  { id: '1',            name: '2022 Polestar 1', power:609, acc:4.2, topSpeed:250, engine: '2.0 Plug-in Hybrid AWD', price: '$109.990', img: '/static/images/polestar1.jpg', rearImg: '/static/rearimg/polestar1-rear.jpg' , consumption: { value:22.0, unit: 'kWh/100km' }},

  { id: '3',            name: '2024 Polestar 3', power:489, acc:5.0, topSpeed:210, engine: '111 kWh', price: '$67.800', img: '/static/images/polestar3.jpg', rearImg: '/static/rearimg/polestar3-rear.png' , consumption: { value:22.0, unit: 'kWh/100km' }},

  { id: '4',            name: '2025 Polestar 4', power:272, acc:7.4, topSpeed:180, engine: '102 kWh', price: '$52.990', img: '/static/images/polestar4.png', rearImg: '/static/rearimg/polestar4-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'Solstice',     name: '2008 Pontiac Solstice', power:173, acc:7.2, topSpeed:198, engine: '2.4 i 16V', price: '$19.490', img: '/static/images/pontiacSolstice.png', rearImg: '/static/rearimg/pontiacSolstice-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: '718',          name: '2021 Porsche 718', power:420, acc:3.9, topSpeed:300, engine: '4.0', price: '$79.900', img: '/static/images/porsche718.png', rearImg: '/static/rearimg/porsche718-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: '718 Spyder',   name: '2023 Porsche 718 Spyder', power:420, acc:4.4, topSpeed:301, engine: '4.0', price: '$119.900', img: '/static/images/porsche718Spyder.png', rearImg: '/static/rearimg/porsche718Spyder-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: '911',          name: '2022 Porsche 911', power:385, acc:4.4, topSpeed:289, engine: '4 3.0 PDK', price: '$118.900', img: '/static/images/porsche911.png', rearImg: '/static/rearimg/porsche911-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '911 Turbo',    name: '2024 Porsche 911 Turbo', power:580, acc:2.8, topSpeed:320, engine: '3.8 Twin-Turbo Flat-6', price: '$197.200', img: '/static/images/porsche911.png', rearImg: '/static/rearimg/porsche911-rear.jpg' , consumption: { value:12.5, unit: 'L/100km' }},

  { id: '930',          name: '1989 Porsche 930', power:282, acc:5.4, topSpeed:260, engine: '3.3 Turbo', price: '$140.000', img: '/static/images/porsche930.png', rearImg: '/static/rearimg/porsche930-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: '964',          name: '1990 Porsche 964', power:250, acc:6.6, topSpeed:256, engine: 'Carrera 2 3.6', price: '$83.880', img: '/static/images/porsche964.png', rearImg: '/static/rearimg/porsche964-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '991',          name: '2015 Porsche 991', power:400, acc:4.8, topSpeed:296, engine: '4S 3.8', price: '$114.991', img: '/static/images/porsche991.jpg', rearImg: '/static/rearimg/porsche991-rear.jpg' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: '992',          name: '2021 Porsche 992', power:510, acc:3.4, topSpeed:318, engine: 'GT3 4.0', price: '$165.970', img: '/static/images/porsche992.png', rearImg: '/static/rearimg/porsche992-rear.png' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: '993',          name: '1996 Porsche 993', power:286, acc:5.4, topSpeed:275, engine: '3.6', price: '$107.500', img: '/static/images/porsche993.jpg', rearImg: '/static/rearimg/porsche993-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '996',          name: '2004 Porsche 996', power:320, acc:5.3, topSpeed:280, engine: 'Carrera 4S 3.6', price: '$49.990', img: '/static/images/porsche996.jpg', rearImg: '/static/rearimg/porsche996-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '997',          name: '2008 Porsche 997', power:480, acc:4.9, topSpeed:297, engine: 'Targa 4S 3.8', price: '$89.950', img: '/static/images/porsche997.png', rearImg: '/static/rearimg/porsche997-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: '912',          name: '1966 Porsche 912', power:90, acc:13.5, topSpeed:185, engine: '1.6', price: '$57.950', img: '/static/images/porsche912.png', rearImg: '/static/rearimg/porsche912-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: '914',          name: '1976 Porsche 914', power:101, acc:12, topSpeed:201, engine: '2.0', price: '$26.000', img: '/static/images/porsche914.jpg', rearImg: '/static/rearimg/porsche914-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: '918',          name: '2015 Porsche 918', power:886, acc:2.6, topSpeed:345, engine: '4.6 V8', price: '$1.320.000', img: '/static/images/porsche918.jpg', rearImg: '/static/rearimg/porsche918-rear.jpg' , consumption: { value:23.5, unit: 'kWh/100km' }},

  { id: '928',          name: '1986 Porsche 928', power:310, acc:6.3, topSpeed:265, engine: '5.0 S4 CAT V8', price: '$48.900', img: '/static/images/porsche928.png', rearImg: '/static/rearimg/porsche928-rear.jpg' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: '944',          name: '1990 Porsche 944', power:165, acc:8.2, topSpeed:218, engine: '2.7', price: '$25.800', img: '/static/images/porsche944.jpg', rearImg: '/static/rearimg/porsche944-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: '962',          name: '1983 Porsche 962', power:650, acc:3.0, topSpeed:360, engine: '3.2L Porsche Flat-6', price: '$450.000', img: '/static/images/porsche962.jpg', rearImg: '/static/rearimg/porsche962-rear.png' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: '968',          name: '1994 Porsche 968', power:239, acc:6.5, topSpeed:252, engine: '3.0 16V', price: '$27.750', img: '/static/images/porsche968.png', rearImg: '/static/rearimg/porsche968-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Boxster',      name: '2015 Porsche Boxster', power:265, acc:5.8, topSpeed:264, engine: '2.7', price: '$39.990', img: '/static/images/porscheBoxster.jpg', rearImg: '/static/rearimg/porscheBoxster-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: '718 Boxster',  name: '2023 Porsche 718 Boxster', power:300, acc:4.9, topSpeed:275, engine: '2.0 Turbo', price: '$76.400', img: '/static/images/porscheBoxster.jpg', rearImg: '/static/rearimg/porscheBoxster-rear.png' , consumption: { value:9.4, unit: 'L/100km' }},

  { id: 'Carrera GT',   name: '2004 Porsche Carrera GT', power:612, acc:3.9, topSpeed:330, engine: '5.7 i V10 40V', price: '$1.450.000', img: '/static/images/porscheCarreraGT.png', rearImg: '/static/rearimg/porscheCarreraGT-rear.jpg' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Cayenne',      name: '2018 Porsche Cayenne', power:462, acc:5.0, topSpeed:253, engine: '3.0 V6', price: '$45.950', img: '/static/images/porscheCayenne.jpg', rearImg: '/static/rearimg/porscheCayenne-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Cayman',       name: '2017 Porsche Cayman', power:349, acc:4.4, topSpeed:295, engine: 'GT4 3.8', price: '$65.000', img: '/static/images/porscheCayman.jpg', rearImg: '/static/rearimg/porscheCayman-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: '718 Cayman',   name: '2023 Porsche 718 Cayman', power:300, acc:4.9, topSpeed:275, engine: '2.0 Turbo', price: '$72.800', img: '/static/images/porscheCayman.jpg', rearImg: '/static/rearimg/porscheCayman-rear.png' , consumption: { value:9.2, unit: 'L/100km' }},

  { id: 'Macan',        name: '2021 Porsche Macan', power:245, acc:6.2, topSpeed:232, engine: 'T 2.0', price: '$56.900', img: '/static/images/porscheMacan.jpg', rearImg: '/static/rearimg/porscheMacan-rear.png' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'Panamera',     name: '2018 Porsche Panamera', power:330, acc:5.3, topSpeed:259, engine: '4 3.0 V6', price: '$59.990', img: '/static/images/porschePanamera.png', rearImg: '/static/rearimg/porschePanamera-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Targa',        name: '2021 Porsche Targa', power:385, acc:4.4, topSpeed:289, engine: '3.0L Twin-Turbo Boxer 6', price: '$144.900', img: '/static/images/porscheTarga.jpg', rearImg: '/static/rearimg/porscheTarga-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Taycan',       name: '2022 Porsche Taycan', power:408, acc:5.4, topSpeed:230, engine: 'Performance 79.2 kWh', price: '$64.900', img: '/static/images/porscheTaycan.png', rearImg: '/static/rearimg/porscheTaycan-rear.png' , consumption: { value:21.5, unit: 'kWh/100km' }},

  { id: '1500',         name: '2025 RAM 1500', power:540, acc:4.9, topSpeed:190, engine: 'RHO 3.0 SST HO', price: '$99.950', img: '/static/images/ram1500.png', rearImg: '/static/rearimg/ram1500-rear.png' , consumption: { value:15.5, unit: 'L/100km' }},

  { id: 'Alpine A610',  name: '1992 Renault Alpine A610', power:250, acc:5.7, topSpeed:265, engine: '3.0L V6 Turbo', price: '$51.900', img: '/static/images/renaultAlpineA610.png', rearImg: '/static/rearimg/renaultAlpineA610-rear.png' , consumption: { value:12.0, unit: 'L/100km' }},

  { id: 'Austral',      name: '2022 Renault Austral', power:158, acc:9.7, topSpeed:175, engine: '1.3', price: '$26.900', img: '/static/images/renaultAustral.png', rearImg: '/static/rearimg/renaultAustral-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Captur',       name: '2025 Renault Captur', power:158, acc:8.9, topSpeed:180, engine: '1.8', price: '$19.950', img: '/static/images/renaultCaptur.png', rearImg: '/static/rearimg/renaultCaptur-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Clio',         name: '2025 Renault Clio', power:115, acc:10.1, topSpeed:180, engine: '1.2 TCe', price: '$28.900', img: '/static/images/renaultClio.jpg', rearImg: '/static/rearimg/renaultClio-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Rafale',       name: '2024 Renault Rafale', power:300, acc:6.4, topSpeed:180, engine: '1.2', price: '$39.900', img: '/static/images/renaultRafale.png', rearImg: '/static/rearimg/renaultRafale-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'R 4',          name: '2025 Renault R 4', power:150, acc:8.5, topSpeed:150, engine: '52 kWh', price: '$31.500', img: '/static/images/renaultR4.png', rearImg: '/static/rearimg/renaultR4-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'R 5',          name: '2025 Renault R 5', power:150, acc:8.0, topSpeed:150, engine: '52 kWh', price: '$29.400', img: '/static/images/renaultR5.png', rearImg: '/static/rearimg/renaultR5-rear.png' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'R1S',          name: '2024 Rivian R1S', power:700, acc:3.7, topSpeed:201, engine: 'Large Pack 135 kWh', price: '$95.590', img: '/static/images/rivianR1S.jpg', rearImg: '/static/rearimg/rivianR1S-rear.png' , consumption: { value:25.0, unit: 'kWh/100km' }},

  { id: 'Camargue',     name: '1981 Rolls-Royce Camargue', power:212, acc:11.0, topSpeed:190, engine: '6.75L V8', price: '$70.900', img: '/static/images/rollsRoyceCamargue.jpg', rearImg: '/static/rearimg/rollsRoyceCamargue-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Cloud',        name: '1957 Rolls-Royce Cloud', power:136, acc:14.0, topSpeed:170, engine: '6.2L V8', price: '$49.500', img: '/static/images/rollsRoyceCloud.png', rearImg: '/static/rearimg/rollsRoyceCloud-rear.jpg' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Corniche',     name: '2000 Rolls-Royce Corniche', power:329, acc:8.5, topSpeed:225, engine: '6.8 i V8 Turbo', price: '$133.900', img: '/static/images/rollsRoyceCorniche.png', rearImg: '/static/rearimg/rollsRoyceCorniche-rear.png' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Cullinan',     name: '2024 Rolls-Royce Cullinan', power:572, acc:5.2, topSpeed:250, engine: '6.7 V12', price: '$559.900', img: '/static/images/rollsRoyceCullinan.png', rearImg: '/static/rearimg/rollsRoyceCullinan-rear.png' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Dawn',         name: '2020 Rolls-Royce Dawn', power:571, acc:4.9, topSpeed:250, engine: '6.6 V12', price: '$339.000', img: '/static/images/rollsRoyceDawn.jpg', rearImg: '/static/rearimg/rollsRoyceDawn-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Ghost',        name: '2022 Rolls-Royce Ghost', power:571, acc:4.8, topSpeed:250, engine: '6.75 V12', price: '$452.081', img: '/static/images/rollsRoyceGhost.jpg', rearImg: '/static/rearimg/rollsRoyceGhost-rear.png' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'Phantom',      name: '2022 Rolls-Royce Phantom', power:571, acc:5.3, topSpeed:250, engine: '6.7 V12', price: '$599.900', img: '/static/images/rollsRoycePhantom.png', rearImg: '/static/rearimg/rollsRoycePhantom-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Phantom Drophead',  name: '2007 Rolls-Royce Phantom Drophead', power:460, acc:5.8, topSpeed:240, engine: '6.7 V12', price: '$258.900', img: '/static/images/rollsRoycePhantomDrophead.png', rearImg: '/static/rearimg/rollsRoycePhantomDrophead-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Silver Dawn',  name: '1951 Rolls-Royce Silver Dawn', power:135, acc:13.0, topSpeed:155, engine: '4.6', price: '$99.000', img: '/static/images/rollsRoyceSilverDawn.png', rearImg: '/static/rearimg/rollsRoyceSilverDawn-rear.png' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Spectre',      name: '2024 Rolls-Royce Spectre', power:258, acc:4.5, topSpeed:250, engine: '102 kWh', price: '$490.000', img: '/static/images/rollsRoyceSpectre.jpg', rearImg: '/static/rearimg/rollsRoyceSpectre-rear.jpg' , consumption: { value:23.0, unit: 'kWh/100km' }},

  { id: 'Wraith',       name: '2017 Rolls-Royce Wraith', power:632, acc:4.5, topSpeed:250, engine: '6.6 V12', price: '$215.980', img: '/static/images/rollsRoyceWraith.jpg', rearImg: '/static/rearimg/rollsRoyceWraith-rear.jpg' , consumption: { value:15.0, unit: 'L/100km' }},

  { id: 'R Kompressor', name: '2003 Ruf R Kompressor', power:409, acc:4.5, topSpeed:310, engine: '3.6L', price: '$165.990', img: '/static/images/rufRKompressor.jpg', rearImg: '/static/rearimg/rufRKompressor-rear.jpg' , consumption: { value:20.0, unit: 'L/100km' }},

  { id: 'Tarraco',      name: '2022 SEAT Tarraco', power:150, acc:10.1, topSpeed:196, engine: '2.0 TDI', price: '$23.445', img: '/static/images/seatTarraco.png', rearImg: '/static/rearimg/seatTarraco-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Ateca',        name: '2022 SEAT Ateca', power:150, acc:8.8, topSpeed:196, engine: '2.0 TDI', price: '$21.990', img: '/static/images/seatAteca.jpg', rearImg: '/static/rearimg/seatAteca-rear.jpg' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Seres 5',      name: '2024 Seres Seres 5', power:585, acc:3.7, topSpeed:200, engine: '90 kWh', price: '$42.800', img: '/static/images/seresSeres5.png', rearImg: '/static/rearimg/seresSeres5-rear.png' , consumption: { value:22.0, unit: 'L/100km' }},

  { id: 'F-150',        name: '2017 Shelby F-150', power:700, acc:4.7, topSpeed:220, engine: '5.0L V8', price: '$90.950', img: '/static/images/shelbyF150.jpg', rearImg: '/static/rearimg/shelbyF150-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'GT 3',         name: '2007 Shelby GT', power:650, acc:4.1, topSpeed:260, engine: '5.4L Supercharged V8', price: '$67.000', img: '/static/images/shelbyGT2.jpg', rearImg: '/static/rearimg/shelbyGT2-rear.png' , consumption: { value:19.0, unit: 'L/100km' }},

  { id: 'Mustang GT-H', name: '1970 Shelby Mustang GT-H', power:334, acc:6.3, topSpeed:205, engine: 'GT 500 7.0 V8', price: '$289.750', img: '/static/images/shelbyMustangGT-H.jpg', rearImg: '/static/rearimg/shelbyMustangGT-H-rear.png' , consumption: { value:17.0, unit: 'L/100km' }},

  { id: 'Elroq',        name: '2026 Skoda Elroq', power:204, acc:5.4, topSpeed:180, engine: 'RS 84 kWh', price: '$37.985', img: '/static/images/skodaElroq.png', rearImg: '/static/rearimg/skodaElroq-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Enyaq',        name: '2021 Skoda Enyaq', power:179, acc:8.8, topSpeed:160, engine: '60 62 kWh', price: '$27.444', img: '/static/images/skodaEnyaq.png', rearImg: '/static/rearimg/skodaEnyaq-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Octavia',      name: '2020 Skoda Octavia', power:116, acc:8.8, topSpeed:222, engine: '2.0 TDI', price: '$18.490', img: '/static/images/skodaOctavia.png', rearImg: '/static/rearimg/skodaOctavia-rear.png' , consumption: { value:5.0, unit: 'L/100km' }},

  { id: 'Superb',       name: '2025 Skoda Superb', power:150, acc:9.2, topSpeed:225, engine: '2.0 TDI', price: '$43.980', img: '/static/images/skodaSuperb.png', rearImg: '/static/rearimg/skodaSuperb-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: '#1',           name: '2025 smart #1', power:428, acc:3.9, topSpeed:180, engine: '66 kWh', price: '$36.799', img: '/static/images/smart1.jpg', rearImg: '/static/rearimg/smart1-rear.jpg' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: '#5',           name: '2025 smart #5', power:646, acc:3.8, topSpeed:210, engine: 'Brabus 100 kWh', price: '$51.890', img: '/static/images/smart5.png', rearImg: '/static/rearimg/smart5-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Sportequipe 7', name: '2026 Sportequipe Sportequipe 7', power:156, acc:10.0, topSpeed:185, engine: '1.5 T', price: '$31.900', img: '/static/images/sportequipe7.png', rearImg: '/static/rearimg/sportequipe7-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Sportequipe 8', name: '2026 Sportequipe Sportequipe 8', power:185, acc:8.0, topSpeed:210, engine: 'GT 1.6', price: '$35.900', img: '/static/images/sportequipe8.png', rearImg: '/static/rearimg/sportequipe8-rear.png' , consumption: { value:8.2, unit: 'L/100km' }},

  { id: 'C8',           name: '2006 Spyker C8', power:400, acc:4.5, topSpeed:300, engine: '4.2i V8 40V', price: '$499.888', img: '/static/images/spykerC8.png', rearImg: '/static/rearimg/spykerC8-rear.jpg' , consumption: { value:16.0, unit: 'L/100km' }},

  { id: 'Rexton',       name: '2021 SsangYong Rexton', power:203, acc:10.8, topSpeed:184, engine: '2.2D', price: '$33.890', img: '/static/images/ssangyongRexton.jpg', rearImg: '/static/rearimg/ssangyongRexton-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'BRZ',          name: '2013 Subaru BRZ', power:200, acc:7.6, topSpeed:226, engine: '2.0', price: '$21.500', img: '/static/images/subaruBRZ.png', rearImg: '/static/rearimg/subaruBRZ-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'BRZ 2',        name: '2023 Subaru BRZ 2', power:234, acc:6.3, topSpeed:226, engine: 'BRZ 2.4 SPORT', price: '$39.400', img: '/static/images/subaruBRZ2.jpg', rearImg: '/static/rearimg/subaruBRZ2-rear.png' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Crosstrek',    name: '2026 Subaru Crosstrek', power:136, acc:10.8, topSpeed:198, engine: '2.0ie', price: '$33.900', img: '/static/images/subaruCrosstrek.jpg', rearImg: '/static/rearimg/subaruCrosstrek-rear.png' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Impreza',      name: '2022 Subaru Impreza', power:150, acc:10.0, topSpeed:188, engine: 'GT 2.0', price: '$19.900', img: '/static/images/subaruImpreza.jpg', rearImg: '/static/rearimg/subaruImpreza-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'Solterra',     name: '2024 Subaru Solterra', power:218, acc:7.0, topSpeed:160, engine: '71.4 kWh', price: '$33.900', img: '/static/images/subaruSolterra.jpg', rearImg: '/static/rearimg/subaruSolterra-rear.jpg' , consumption: { value:16.0, unit: 'kWh/100km' }},

  { id: 'WRX',          name: '2025 Subaru WRX', power:300, acc:5.2, topSpeed:255, engine: '2.5', price: '$52.900', img: '/static/images/subaruWRX.jpg', rearImg: '/static/rearimg/subaruWRX-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'Across',       name: '2023 Suzuki Across', power:185, acc:6, topSpeed:180, engine: '2.5', price: '$36.980', img: '/static/images/suzukiAcross.png', rearImg: '/static/rearimg/suzukiAcross-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'SX4 S-Cross',  name: '2022 Suzuki SX4 S-Cross', power:129, acc:9.5, topSpeed:195, engine: '1.4 Boosterjet', price: '$20.020', img: '/static/images/suzukiSX4SCross.png', rearImg: '/static/rearimg/suzukiSX4SCross-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'G01F',         name: '2025 SWM G01F', power:139, acc:11.0, topSpeed:180, engine: '1.5 Turbo', price: '$25.950', img: '/static/images/suzukiG01F.png', rearImg: '/static/rearimg/suzukiG01F-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: 'Cybertruck',   name: '2026 Tesla Cybertruck', power:600, acc:4.3, topSpeed:180, engine: '123 kWh', price: '$204.000', img: '/static/images/teslaCybertruck.jpg', rearImg: '/static/rearimg/teslaCybertruck-rear.png' , consumption: { value:27, unit: 'kWh/100km' }},
  
  { id: 'Model S',      name: '2018 Tesla Model S', power:417, acc:4.4, topSpeed:250, engine: '90D 90 kWh', price: '$29.950', img: '/static/images/teslaModelS.png', rearImg: '/static/rearimg/teslaModelS-rear.png' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Model X',      name: '2017 Tesla Model X', power:215, acc:4.6, topSpeed:250, engine: 'Long Range 100 kWh', price: '$35.900', img: '/static/images/teslaModelX.jpg', rearImg: '/static/rearimg/teslaModelX-rear.png' , consumption: { value:24.0, unit: 'kWh/100km' }},

  { id: 'Model Y',      name: '2025 Tesla Model Y', power:460, acc:3.5, topSpeed:250, engine: 'Performance 84.7 kWh', price: '$54.990', img: '/static/images/teslaModelY.jpg', rearImg: '/static/rearimg/teslaModelY-rear.jpg' , consumption: { value:19.0, unit: 'kWh/100km' }},

  { id: 'Roadster',     name: '2012 Tesla Roadster', power:292, acc:3.7, topSpeed:201, engine: 'Sport 53 kWh', price: '$99.950', img: '/static/images/teslaRoadster.png', rearImg: '/static/rearimg/teslaRoadster-rear.png' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'Six',          name: '2025 Tiger Six', power:177, acc:10.0, topSpeed:190, engine: '1.5 T-GDI', price: '$29.900', img: '/static/images/tigerSix.jpg', rearImg: '/static/rearimg/tigerSix-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'T10X',         name: '2024 Togg T10X', power:218, acc:7.4, topSpeed:185, engine: 'Standard Range 52.4 kWh', price: '$49.980', img: '/static/images/toggT10X.png', rearImg: '/static/rearimg/toggT10X-rear.png' , consumption: { value:18.0, unit: 'kWh/100km' }},

  { id: '4-Runner',     name: '2026 Toyota 4-Runner', power:326, acc:6.5, topSpeed:180, engine: '2.4L Turbo', price: '$90.900', img: '/static/images/toyota4Runner.jpg', rearImg: '/static/rearimg/toyota4Runner-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'bZ4X',         name: '2024 Toyota bZ4X', power:224, acc:7.4, topSpeed:160, engine: '73 kWh', price: '$34.500', img: '/static/images/toyotaBZ4X.jpg', rearImg: '/static/rearimg/toyotaBZ4X-rear.jpg' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'Camry',        name: '2019 Toyota Camry', power:218, acc:8.3, topSpeed:180, engine: '2.5 Hybrid e-CVT', price: '$26.990', img: '/static/images/toyotaCamry.jpg', rearImg: '/static/rearimg/toyotaCamry-rear.jpg' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Corolla',      name: '2022 Toyota Corolla', power:122, acc:10.5, topSpeed:180, engine: '1.8 Hybrid', price: '$18.670', img: '/static/images/toyotaCorolla.jpg', rearImg: '/static/rearimg/toyotaCorolla-rear.png' , consumption: { value:13.0, unit: 'L/100km' }},

  { id: 'Corolla Cross', name: '2023 Toyota Corolla Cross', power:199, acc:7.6, topSpeed:180, engine: '2.0', price: '$29.900', img: '/static/images/toyotaCorollaCross.jpg', rearImg: '/static/rearimg/toyotaCorollaCross-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'FJ Cruiser',   name: '2013 Toyota FJ Cruiser', power:261, acc:8.2, topSpeed:175, engine: '4.0L V6', price: '$39.950', img: '/static/images/toyotaFJCruiser.png', rearImg: '/static/rearimg/toyotaFJ-rear.jpg' , consumption: { value:14.0, unit: 'L/100km' }},

  { id: 'GR86',         name: '2024 Toyota GR86', power:234, acc:6.7, topSpeed:226, engine: '2.4L', price: '$37.500', img: '/static/images/toyotaGR86.jpg', rearImg: '/static/rearimg/toyotaGR86-rear.png' , consumption: { value:8.5, unit: 'L/100km' }},

  { id: 'GT86',         name: '2013 Toyota GT86', power:200, acc:7.4, topSpeed:220, engine: '2.0L', price: '$24.990', img: '/static/images/toyotaGT86.jpg', rearImg: '/static/rearimg/toyotaGT86-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'Land Cruiser', name: '2026 Toyota Land Cruiser', power:205, acc:10.5, topSpeed:170, engine: '2.8L Turbo', price: '$83.480', img: '/static/images/toyotaLandCruiser.jpg', rearImg: '/static/rearimg/toyotaLandCruiser-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Mirai',        name: '2021 Toyota Mirai', power:182, acc:9.2, topSpeed:175, engine: '1.2 kWh', price: '$24.595', img: '/static/images/toyotaMirai.jpg', rearImg: '/static/rearimg/toyotaMirai-rear.jpg' , consumption: { value:0.0, unit: 'L/100km' }},

  { id: 'Sequoia',      name: '2026 Toyota Sequoia', power:435, acc:5.9, topSpeed:185, engine: '3.4L V6 Twin-Turbo', price: '$124.800', img: '/static/images/toyotaSequoia.jpg', rearImg: '/static/rearimg/toyotaSequoia-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'Supra',        name: '2024 Toyota Supra', power:260, acc:4.3, topSpeed:250, engine: 'GR 3.0', price: '$55.990', img: '/static/images/toyotaSupra.jpg', rearImg: '/static/rearimg/toyotaSupra-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'Tacoma',       name: '2026 Toyota Tacoma', power:326, acc:7.2, topSpeed:185, engine: '2.4L Turbo', price: '$98.615', img: '/static/images/toyotaTacoma.png', rearImg: '/static/rearimg/toyotaTacoma-rear.png' , consumption: { value:11.0, unit: 'L/100km' }},

  { id: 'VF 8',         name: '2026 VinFast VF 8', power:408, acc:5.7, topSpeed:200, engine: 'Standard Range 82 kWh', price: '$48.900', img: '/static/images/vinfastVF8.png', rearImg: '/static/rearimg/vinfastVF8-rear.jpg' , consumption: { value:21.0, unit: 'kWh/100km' }},

  { id: 'Arteon',       name: '2019 Volkswagen Arteon', power:272, acc:5.6, topSpeed:250, engine: '2.0 TSI', price: '$26.990', img: '/static/images/vwArteon.jpg', rearImg: '/static/rearimg/vwArteon-rear.jpg' , consumption: { value:8.0, unit: 'L/100km' }},

  { id: 'Golf GTD',     name: '2022 Volkswagen Golf GTD', power:200, acc:7.1, topSpeed:245, engine: 'GTD 2.0 TDI', price: '$35.990', img: '/static/images/vwGolfGTD.png', rearImg: '/static/rearimg/vwGolfGTD-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Golf R',       name: '2025 Volkswagen Golf R', power:245, acc:8.5, topSpeed:224, engine: '1.5 TSI', price: '$38.590', img: '/static/images/vwGolfR.jpg', rearImg: '/static/rearimg/vwGolfR-rear.jpg' , consumption: { value:9.0, unit: 'L/100km' }},

  { id: 'ID.7',         name: '2024 Volkswagen ID.7', power:286, acc:6.6, topSpeed:180, engine: 'Pro S 91 kWh', price: '$43.950', img: '/static/images/vwID7.png', rearImg: '/static/rearimg/vwID7-rear.png' , consumption: { value:18.0, unit: 'L/100km' }},

  { id: 'Passat',       name: '2020 Volkswagen Passat', power:218, acc:7.4, topSpeed:222, engine: 'GTE 1.4 TSI', price: '$19.980', img: '/static/images/vwPassat.png', rearImg: '/static/rearimg/vwPassat-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Polo GTI',     name: '2024 Volkswagen Polo GTI', power:207, acc:6.5, topSpeed:240, engine: 'GTI 2.0 TSI', price: '$26.490', img: '/static/images/vwPoloGTI.png', rearImg: '/static/rearimg/vwPoloGTI-rear.png' , consumption: { value:7.8, unit: 'L/100km' }},

  { id: 'Tayron',       name: '2025 Volkswagen Tayron', power:150, acc:9.4, topSpeed:204, engine: '1.5 eTSI', price: '$39.990', img: '/static/images/vwTayron.png', rearImg: '/static/rearimg/vwTayron-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'C40',          name: '2022 Volvo C40', power:231, acc:7.4, topSpeed:160, engine: '69 kWh', price: '$31.490', img: '/static/images/volvoC40.jpg', rearImg: '/static/rearimg/volvoC40-rear.png' , consumption: { value:16.5, unit: 'kWh/100km' }},

  { id: 'EC40',         name: '2023 Volvo EC40', power:252, acc:7.3, topSpeed:180, engine: '82 kWh', price: '$38.900', img: '/static/images/volvoEC40.jpg', rearImg: '/static/rearimg/volvoEC40-rear.jpg' , consumption: { value:17.2, unit: 'kWh/100km' }},

  { id: 'ES90',         name: '2026 Volvo ES90', power:333, acc:6.9, topSpeed:180, engine: '92 kWh', price: '$84.990', img: '/static/images/volvoES90.jpg', rearImg: '/static/rearimg/volvoES90-rear.jpg' , consumption: { value:18.0, unit: 'kWh/100km' }},

  { id: 'EX30',         name: '2024 Volvo EX30', power:272, acc:5.3, topSpeed:180, engine: '69 kWh', price: '$33.950', img: '/static/images/volvoEX30.png', rearImg: '/static/rearimg/volvoEX30-rear.png' , consumption: { value:15.8, unit: 'kWh/100km' }},

  { id: 'EX40',         name: '2025 Volvo EX40', power:252, acc:7.3, topSpeed:180, engine: '82 kWh', price: '$37.700', img: '/static/images/volvoEX40.jpg', rearImg: '/static/rearimg/volvoEX40-rear.png' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: 'EX90',         name: '2025 Volvo EX90', power:333, acc:6.8, topSpeed:180, engine: '92 kWh', price: '$75.900', img: '/static/images/volvoEX90.jpg', rearImg: '/static/rearimg/volvoEX90-rear.png' , consumption: { value:19.5, unit: 'kWh/100km' }},

  { id: 'S90',          name: '2021 Volvo S90', power:390, acc:4.7, topSpeed:180, engine: 'Recharge 2.0 T8', price: '$34.940', img: '/static/images/volvoS90.jpg', rearImg: '/static/rearimg/volvoS90-rear.jpg' , consumption: { value:20.0, unit: 'kWh/100km' }},

  { id: 'XC60',         name: '2021 Volvo XC60', power:197, acc:8.3, topSpeed:180, engine: '2.0d B4', price: '$34.250', img: '/static/images/volvoXC60.jpg', rearImg: '/static/rearimg/volvoXC60-rear.png' , consumption: { value:9.5, unit: 'L/100km' }},

  { id: 'XC90',         name: '2016 Volvo XC90', power:407, acc:5.6, topSpeed:230, engine: '2.0 T8 Twin Engine', price: '$25.740', img: '/static/images/volvoXC90.png', rearImg: '/static/rearimg/volvoXC90-rear.png' , consumption: { value:19.5, unit: 'kWh/100km' }},

  { id: 'Courage',      name: '2026 Voyah Courage', power:292, acc:6.8, topSpeed:204, engine: '77 kWh', price: '$44.990', img: '/static/images/voyahCourage.png', rearImg: '/static/rearimg/voyahCourage-rear.png' , consumption: { value:17.8, unit: 'kWh/100km' }},

  { id: 'MF 3',         name: '2010 Wiesmann MF 3', power:343, acc:4.9, topSpeed:255, engine: '3.2i 24V', price: '$138.000', img: '/static/images/wiesmannMF3.png', rearImg: '/static/rearimg/wiesmannMF3-rear.png' , consumption: { value:11.5, unit: 'L/100km' }},

  { id: 'MF 5',         name: '2009 Wiesmann MF 5', power:507, acc:3.9, topSpeed:311, engine: '4.4 V8', price: '$289.500', img: '/static/images/wiesmannMF5.png', rearImg: '/static/rearimg/wiesmannMF5-rear.png' , consumption: { value:12.8, unit: 'L/100km' }},

  { id: 'SU7',          name: '2025 Xiaomi SU7', power:673, acc:2.7, topSpeed:265, engine: 'Max 101 kWh', price: '$64.999', img: '/static/images/xiaomiSU7.jpg', rearImg: '/static/rearimg/xiaomiSU7-rear.jpg' , consumption: { value:15.0, unit: 'kWh/100km' }},

  { id: 'G6',           name: '2025 Xpeng G6', power:296, acc:6.3, topSpeed:202, engine: 'Long Range 68.5 kWh', price: '$43.590', img: '/static/images/xpengG6.jpg', rearImg: '/static/rearimg/xpengG6-rear.png' , consumption: { value:16.2, unit: 'kWh/100km' }},

  { id: 'P7',           name: '2025 Xpeng P7', power:367, acc:5.4, topSpeed:230, engine: '92.2 kWh', price: '$39.900', img: '/static/images/xpengP7.jpg', rearImg: '/static/rearimg/xpengP7-rear.jpg' , consumption: { value:17.0, unit: 'kWh/100km' }},

  { id: '001',          name: '2024 Zeekr 001', power:422, acc:5.9, topSpeed:240, engine: '100 kWh', price: '$55.990', img: '/static/images/zeekr001.png', rearImg: '/static/rearimg/zeekr001-rear.jpg' , consumption: { value:18.0, unit: 'kWh/100km' }},

  { id: 'X',            name: '2025 Zeekr X', power:428, acc:3.8, topSpeed:180, engine: '69 kWh', price: '$45.000', img: '/static/images/zeekrX.jpg', rearImg: '/static/rearimg/zeekrX-rear.jpg' , consumption: { value:16.0, unit: 'kWh/100km' }}

];

const Motorcycles = [
  { id: 'Legend Tejas',     name: '2006 American Ironhorse Legend Tejas', power:67, acc:5.0, topSpeed:180, engine: 'V-Twin', price: '€18,990', mimages: '/static/images/legendTejas.png', mrearImg: '/static/rearimg/legendTejas-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'RS 660',           name: '2023 Aprilia RS 660', power:109, acc:3.7, topSpeed:235, engine: '659 cc', price: '€14,590', mimages: '/static/images/rs660.jpg', mrearImg: '/static/rearimg/rs660-rear.jpg' , consumption: { value:4.8, unit: 'L/100km' }},

  { id: 'Napoleonbob 500',  name: '2026 Benda', power:48, acc:6.5, topSpeed:165, engine: '500 cc', price: '€7,780', mimages: '/static/images/Napoleonbob500.jpg', mrearImg: '/static/rearimg/Napoleonbob500-rear.jpg' , consumption: { value:5.1, unit: 'L/100km' }},

  { id: 'Leoncino 800',     name: '2026 Benelli Leoncino 800', power:76, acc:4.5, topSpeed:205, engine: '754 cc', price: '€6,780', mimages: '/static/images/leoncino800.jpg', mrearImg: '/static/rearimg/leoncino800-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: ' RR 125',          name: '2024 Beta RR 125', power:15, acc:14.0, topSpeed:110, engine: '125 cc Minarelli single-cylinder', price: '€5.190', mimages: '/static/images/rr125.jpg', mrearImg: '/static/rearimg/rr125-rear.png' , consumption: { value:3.0, unit: 'L/100km' }},

  { id: 'Dog Motorcycles',  name: '2026 Big Dog Motorcycles', power:71, acc:4.5, topSpeed:175, engine: '1916 cc', price: '€16.995', mimages: '/static/images/bigDogMotorcycles.png', mrearImg: '/static/rearimg/bigDogMotorcycles-rear.png' , consumption: { value:7.5, unit: 'L/100km' }},

  { id: 'TESI H2',          name: '2022 Bimota TESI H2', power:200, acc:3.0, topSpeed:280, engine: '998 cc', price: '€39.995', mimages: '/static/images/bimotaTESIH2.png', mrearImg: '/static/rearimg/bimotaTESIH2-rear.png' , consumption: { value:8.5, unit: 'L/100km' }},

  { id: 'S 1000 R',         name: '2025 BMW S 1000 R', power:170, acc:3.0, topSpeed:250, engine: '999 cc', price: '€21.490', mimages: '/static/images/bmwS1000R.jpg', mrearImg: '/static/rearimg/bmwS1000R-rear.jpg' , consumption: { value:6.2, unit: 'L/100km' }},

  { id: 'R 1250 GS',        name: '2020 BMW R 1250 GS', power:136, acc:3.6, topSpeed:210, engine: '1254 cc', price: '€15.999', mimages: '/static/images/bmwR1250GS.jpg', mrearImg: '/static/rearimg/bmwR1250GS-rear.png' , consumption: { value:4.9, unit: 'L/100km' }},

  { id: 'S1000RR K67',      name: '2020 BMW S1000RR K67', power:207, acc:2.9, topSpeed:299, engine: '999 cc', price: '€17.989', mimages: '/static/images/bmwS1000RRK67.jpg', mrearImg: '/static/rearimg/bmwS1000RRK67-rear.jpg' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'S1000RR',          name: '2015 BMW S1000RR', power:199, acc:8.0, topSpeed:299, engine: '999 cc', price: '€18.790', mimages: '/static/images/BMWS1000RR.png', mrearImg: '/static/rearimg/BMWS1000RR-rear.png' , consumption: { value:6.2, unit: 'L/100km' }},

  { id: 'R 1250 RS',        name: '2019 BMW R 1250 RS', power:136, acc:3.4, topSpeed:235, engine: '1254 cc', price: '€12.689', mimages: '/static/images/BMWR1250RS.png', mrearImg: '/static/rearimg/BMWR1250RS-rear.png' , consumption: { value:5.0, unit: 'L/100km' }},

  { id: 'Cromwell 1200 ABS', name: '2023 Brixton Cromwell 1200 ABS', power:83, acc:5.5, topSpeed:190, engine: '1222 cc', price: '€7.380', mimages: '/static/images/brixtonCromwell1200ABS.jpg', mrearImg: '/static/rearimg/brixtonCromwell1200ABS-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Aston Martin AMB 001',  name: '2021 Brough Superior Aston Martin AMB 001', power:224, acc:3.1, topSpeed:290, engine: '997 cc', price: '€199.900', mimages: '/static/images/broughSuperior.png', mrearImg: '/static/rearimg/broughSuperior-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'XB 12 S',          name: '2008 Buell XB 12 S', power:95, acc:3.8, topSpeed:205, engine: '1203 cc V-Twin', price: '€8.999', mimages: '/static/images/buellXB12S.jpg', mrearImg: '/static/rearimg/buellXB12S-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: '1125 CR',          name: '2011 Buell 1125 CR', power:95, acc:3.3, topSpeed:210, engine: '1250 cc V-Twin', price: '€6.790', mimages: '/static/images/buell1125CR.png', mrearImg: '/static/rearimg/buell1125CR-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'Mito 125',         name: '2007 Cagiva Mito 125', power:14, acc:8.0, topSpeed:160, engine: '125 cc', price: '€8.990', mimages: '/static/images/cagivaMito125.png', mrearImg: '/static/rearimg/cagivaMito125-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: '675 SRR',          name: '2025 CFMOTO 675 SRR', power:90, acc:3.9, topSpeed:225, engine: '675 cc', price: '€7.999', mimages: '/static/images/cfmoto675SRR.jpg', mrearImg: '/static/rearimg/cfmoto675SRR-rear.png' , consumption: { value:4.8, unit: 'L/100km' }},

  { id: '450 MT',           name: '2024 CFMOTO 450 MT', power:42, acc:6.0, topSpeed:165, engine: '449 cc', price: '€5.790', mimages: '/static/images/cfmoto450MT.png', mrearImg: '/static/rearimg/cfmoto450MT-rear.png' , consumption: { value:4.0, unit: 'L/100km' }},

  { id: 'Multistrada V4',   name: '2026 Ducati Multistrada V4', power:170, acc:3.4, topSpeed:240, engine: '1158 cc', price: '€29.999', mimages: '/static/images/ducatiMultistradaV4.jpg', mrearImg: '/static/rearimg/ducatiMultistradaV4-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'Panigale V4R',     name: '2021 Ducati Panigale V4R', power:221, acc:3.0, topSpeed:300, engine: '998 cc', price: '€37.000', mimages: '/static/images/ducatiPanigaleV4R.jpg', mrearImg: '/static/rearimg/ducatiPanigaleV4R-rear.jpg' , consumption: { value:7.8, unit: 'L/100km' }},

  { id: 'Multistrada 1260 S',   name: '2019 Ducati Multistrada 1260 S', power:158, acc:4.0, topSpeed:245, engine: '1262 cc', price: '€17.500', mimages: '/static/images/ducatiMultistrada1260S.jpg', mrearImg: '/static/rearimg/ducatiMultistrada1260S-rear.jpg' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'DIAVEL AMG',      name: '2012 Ducati DIAVEL AMG', power:158, acc:2.9, topSpeed:240, engine: '1198 cc', price: '€20.000', mimages: '/static/images/ducatiDIAVELAMG.jpg', mrearImg: '/static/rearimg/ducatiDIAVELAMG-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: '848 EVO',         name: '2011 Ducati 848 EVO', power:101, acc:3.5, topSpeed:265, engine: '849 cc', price: '€9.390', mimages: '/static/images/ducati848EVO.jpg', mrearImg: '/static/rearimg/ducati848EVO-rear.jpg' , consumption: { value:6.8, unit: 'L/100km' }},

  { id: 'STREETFIGHTER V2',  name: '2022 Ducati STREETFIGHTER V2', power:152, acc:3.3, topSpeed:275, engine: '955 cc', price: '€14.989', mimages: '/static/images/ducatiSTREETFIGHTERV2.jpg', mrearImg: '/static/rearimg/ducatiSTREETFIGHTERV2-rear.jpg' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: 'PANIGALE V2',     name: '2019 Ducati PANIGALE V2', power:155, acc:3.2, topSpeed:285, engine: '955 cc', price: '€16.000', mimages: '/static/images/ducatiPANIGALEV2.jpg', mrearImg: '/static/rearimg/ducatiPANIGALEV2-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'Eva Ribelle',     name: '2023 Energica Eva Ribelle', power:150, acc:2.7, topSpeed:200, engine: 'Electric motor', price: '€22.189', mimages: '/static/images/energicaEvaRibelle.jpg', mrearImg: '/static/rearimg/energicaEvaRibelle-rear.png' , consumption: { value:8.5, unit: 'kWh/100km' }},

  { id: 'Experia',         name: '2024 Energica Experia', power:82, acc:3.7, topSpeed:180, engine: 'Electric motor', price: '€27.990', mimages: '/static/images/energicaExperia.jpg', mrearImg: '/static/rearimg/energicaExperia-rear.png' , consumption: { value:9.0, unit: 'kWh/100km' }},

  { id: ' XEF 250',        name: '2024 Fantic XEF 250', power:16, acc:19.0, topSpeed:114, engine: '249.6 cc', price: '€6.980', mimages: '/static/images/fanticXEF250.jpg', mrearImg: '/static/rearimg/fanticXEF250-rear.jpg' , consumption: { value:3.0, unit: 'L/100km' }},

  { id: 'Stealth 125',     name: '2025 Fantic Stealth 125', power:15, acc:19.4, topSpeed:115, engine: '124.66 cc', price: '€', mimages: '/static/images/fanticStealth125.png', mrearImg: '/static/rearimg/fanticStealth125-rear.png' , consumption: { value:2.7, unit: 'L/100km' }},

  { id: 'Sport Classic 300i',     name: '2025 FB Mondial Sport Classic 300i', power:23, acc:11.0, topSpeed:130, engine: '249 cc', price: '€4.450', mimages: '/static/images/fbMondialSportClassic300i.png', mrearImg: '/static/rearimg/fbMondialSportClassic300i-rear.png' , consumption: { value:4.2, unit: 'L/100km' }},

  { id: 'SM 700',          name: '2024 Gasgas SM 700', power:75, acc:4.6, topSpeed:185, engine: '691 cc', price: '€8.000', mimages: '/static/images/gasgasSM700.jpg', mrearImg: '/static/rearimg/gasgasSM700-rear.jpg' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: 'Taurus 1300',     name: '2014 GG Motorradtechnik Taurus 1300', power:175, acc:5.0, topSpeed:220, engine: '1293 cc', price: '€49.900', mimages: '/static/images/ggMotorradtechnikTaurus1300.png', mrearImg: '/static/rearimg/ggMotorradtechnikTaurus1300-rear.png' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: 'Saturno Bialbero 500', name: '1992 Gilera Saturno Bialbero 500', power:38, acc:6.8, topSpeed:180, engine: '492 cc', price: '€7.850', mimages: '/static/images/gileraSaturnoBialbero500.png', mrearImg: '/static/rearimg/gileraSaturnoBialbero500-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: 'STREET 750',      name: '2017 Harley-Davidson STREET 750', power:58, acc:5.0, topSpeed:180, engine: '749 cc', price: '€6.689', mimages: '/static/images/harleyDavidsonSTREET750.jpg', mrearImg: '/static/rearimg/harleyDavidsonSTREET750-rear.png' , consumption: { value:4.7, unit: 'L/100km' }},

  { id: 'SPORTSTER XL 1200', name: '2015 Harley-Davidson SPORTSTER XL 1200', power:68, acc:4.5, topSpeed:190, engine: '1202 cc', price: '€11.689', mimages: '/static/images/harleyDavidsonSPORTSTERXL1200.png', mrearImg: '/static/rearimg/harleyDavidsonSPORTSTERXL1200-rear.png' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'Softail FXSB',    name: '2015 Harley-Davidson Softail FXSB', power:75, acc:4.7, topSpeed:180, engine: '1690 cc', price: '€37.990', mimages: '/static/images/harleyDavidsonSoftailFXSB.png', mrearImg: '/static/rearimg/harleyDavidsonSoftailFXSB-rear.png' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: 'CRF1100L',        name: '2025 Honda CRF1100L', power:102, acc:4.0, topSpeed:205, engine: '1084 cc', price: '€15.690', mimages: '/static/images/hondaCRF1100L.jpg', mrearImg: '/static/rearimg/hondaCRF1100L-rear.png' , consumption: { value:4.8, unit: 'L/100km' }},

  { id: 'CB 1000 R',       name: '2019 Honda CB 1000 R', power:145, acc:3.0, topSpeed:245, engine: '998 cc', price: '€9.489', mimages: '/static/images/hondaCB1000R.jpg', mrearImg: '/static/rearimg/hondaCB1000R-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: 'CB500X',          name: '2019 Honda CB500X', power:48, acc:5.5, topSpeed:175, engine: '471 cc', price: '€5.299', mimages: '/static/images/hondaCB500X.png', mrearImg: '/static/rearimg/hondaCB500X-rear.png' , consumption: { value:4.0, unit: 'L/100km' }},

  { id: 'NX 500',          name: '2024 Honda NX 500', power:48, acc:6.0, topSpeed:180, engine: '471 cc', price: '€6.390', mimages: '/static/images/hondaNX500.jpg', mrearImg: '/static/rearimg/hondaNX500-rear.png' , consumption: { value:3.7, unit: 'L/100km' }},

  { id: 'CBR 600 RR',      name: '2025 Honda CBR 600 RR', power:121, acc:3.3, topSpeed:260, engine: '599 cc', price: '€11.500', mimages: '/static/images/hondaCBR600RR.jpg', mrearImg: '/static/rearimg/hondaCBR600RR-rear.jpg' , consumption: { value:6.0, unit: 'L/100km' }},

  { id: 'CBR650R',         name: '2024 Honda CBR650R', power:95, acc:3.8, topSpeed:215, engine: '649 cc', price: '€8.999', mimages: '/static/images/hondaCBR650R.jpg', mrearImg: '/static/rearimg/hondaCBR650R-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: 'Norden 901',      name: '2026 Husqvarna Norden 901', power:105, acc:3.6, topSpeed:210, engine: '889 cc', price: '€9.790', mimages: '/static/images/husqvarnaNorden901.png', mrearImg: '/static/rearimg/husqvarnaNorden901-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: 'VITPILEN 801',    name: '2025 Husqvarna VITPILEN 801', power:105, acc:3.4, topSpeed:225, engine: '799 cc', price: '€8.489', mimages: '/static/images/husqvarnaVITPILEN801.png', mrearImg: '/static/rearimg/husqvarnaVITPILEN801-rear.png' , consumption: { value:4.8, unit: 'L/100km' }},

  { id: 'GV 125 S',        name: '2026 Hyosung GV 125 S', power:14, acc:14.0, topSpeed:105, engine: '125 cc', price: '€3.980', mimages: '/static/images/hyosungGV125S.jpg', mrearImg: '/static/rearimg/hyosungGV125S-rear.png' , consumption: { value:2.6, unit: 'L/100km' }},

  { id: 'Scout Sixty',     name: '2016 Indian Scout Sixty', power:77, acc:4.5, topSpeed:190, engine: '999 cc', price: '€9.750', mimages: '/static/images/indianScoutSixty.jpg', mrearImg: '/static/rearimg/indianScoutSixty-rear.jpg' , consumption: { value:4.7, unit: 'L/100km' }},

  { id: 'Dragster 200',    name: '2024 Italjet Dragster 200', power:18, acc:10.0, topSpeed:125, engine: '181 cc', price: '€4.224', mimages: '/static/images/italjetDragster200.jpg', mrearImg: '/static/rearimg/italjetDragster200-rear.png' , consumption: { value:3.2, unit: 'L/100km' }},

  { id: 'Ninja 650',       name: '2025 Kawasaki Ninja 650', power:68, acc:3.8, topSpeed:215, engine: '649 cc', price: '€7.190', mimages: '/static/images/kawasakiNinja650.jpg', mrearImg: '/static/rearimg/kawasakiNinja650-rear.jpg' , consumption: { value:4.3, unit: 'L/100km' }},

  { id: 'Z900',            name: '2021 Kawasaki Z900', power:125, acc:3.0, topSpeed:250, engine: '948 cc', price: '€8.000', mimages: '/static/images/kawasakiZ900.jpg', mrearImg: '/static/rearimg/kawasakiZ900-rear.png' , consumption: { value:5.2, unit: 'L/100km' }},

  { id: 'Z H2',            name: '2020 Kawasaki Z H2', power:200, acc:2.8, topSpeed:290, engine: '998 cc', price: '€13.890', mimages: '/static/images/kawasakiZH2.png', mrearImg: '/static/rearimg/kawasakiZH2-rear.png' , consumption: { value:7.5, unit: 'L/100km' }},

  { id: 'Z 1000 SX',       name: '2019 Kawasaki Z 1000', power:143, acc:3.0, topSpeed:250, engine: '1.043', price: '€9.990', mimages: '/static/images/kawasakiZ1000SX.png', mrearImg: '/static/rearimg/kawasakiZ1000SX-rear.png' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: 'Ninja H2R',       name: '2024 Kawasaki Ninja H2R', power:310, acc:2.5, topSpeed:400, engine: '998 cc', price: '€75.000', mimages: '/static/images/kawasakiNinjaH2R.jpg', mrearImg: '/static/rearimg/kawasakiNinjaH2R-rear.jpg' , consumption: { value:10.0, unit: 'L/100km' }},

  { id: 'RKF 125',         name: '2026 Keeway RKF 125', power:12, acc:15.0, topSpeed:110, engine: '125 cc', price: '€3.180', mimages: '/static/images/keewayRKF125.jpg', mrearImg: '/static/rearimg/keewayRKF125-rear.png' , consumption: { value:2.4, unit: 'L/100km' }},

  { id: '990 Duke',        name: '2024 KTM 990 Duke', power:123, acc:3.0, topSpeed:230, engine: '947 cc', price: '€6.900', mimages: '/static/images/ktm990Duke.jpg', mrearImg: '/static/rearimg/ktm990Duke-rear.png' , consumption: { value:5.5, unit: 'L/100km' }},

  { id: 'Duke 790',        name: '2021 KTM Duke 790', power:105, acc:3.4, topSpeed:230, engine: '799 cc', price: '€5.990', mimages: '/static/images/ktmDuke790.png', mrearImg: '/static/rearimg/ktmDuke790-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: '1290 Super',      name: '2022 KTM 1290 Super', power:160, acc:3.5, topSpeed:240, engine: '799cc', price: '€11.295', mimages: '/static/images/ktm1290Super.jpg', mrearImg: '/static/rearimg/ktm1290Super-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'Drakon 125',      name: '2026 Malaguti Drakon 125', power:14, acc:14.0, topSpeed:115, engine: '124 cc', price: '€3.280', mimages: '/static/images/malagutiDrakon125.png', mrearImg: '/static/rearimg/malagutiDrakon125-rear.png' , consumption: { value:2.8, unit: 'L/100km' }},

  { id: 'DL 125',          name: '2023 Motobi DL 125', power:15, acc:3.5, topSpeed:120, engine: '125 cc', price: '€3.100', mimages: '/static/images/motobiDL125.png', mrearImg: '/static/rearimg/motobiDL125-rear.png' , consumption: { value:3.0, unit: 'L/100km' }},

  { id: 'V100 Mandello',   name: '2023 Moto Guzzi V100 Mandello', power:116, acc:4.0, topSpeed:230, engine: '1.042 cc', price: '€9.480', mimages: '/static/images/motoGuzziV100Mandello.jpg', mrearImg: '/static/rearimg/motoGuzziV100Mandello-rear.png' , consumption: { value:5.0, unit: 'L/100km' }},

  { id: 'V7 IV',           name: '2025 Moto Guzzi V7 IV', power:68, acc:5.7, topSpeed:170, engine: '853 cc', price: '€9.189', mimages: '/static/images/motoGuzziV7IV.png', mrearImg: '/static/rearimg/motoGuzziV7IV-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: 'SEIEMMEZZO STR',  name: '2025 Moto Morini SEIEMMEZZO STR', power:61, acc:5.0, topSpeed:180, engine: '649 cc', price: '€5.480', mimages: '/static/images/motoMoriniSEIEMMEZZOSTR.png', mrearImg: '/static/rearimg/motoMoriniSEIEMMEZZOSTR-rear.png' , consumption: { value:4.4, unit: 'L/100km' }},

  { id: 'X-Cape 700',      name: '2025 Moto Morini X-Cape 700', power:69, acc:4.7, topSpeed:190, engine: '694 cc', price: '€7.792', mimages: '/static/images/motoMoriniXcape700.jpg', mrearImg: '/static/rearimg/motoMoriniXcape700-rear.png' , consumption: { value:4.6, unit: 'L/100km' }},

  { id: 'Brutale 1000 RS', name: '2023 MV Agusta Brutale 1000 RS', power:208, acc:3.0, topSpeed:300, engine: '998 cc', price: '€17.950 ', mimages: '/static/images/mvAgustaBrutale1000RS.jpg', mrearImg: '/static/rearimg/mvAgustaBrutale1000RS-rear.jpg' , consumption: { value:6.8, unit: 'L/100km' }},

  { id: 'F3 800 R',        name: '2017 MV Agusta F3 800 R EAS ABS', power:148, acc:3.1, topSpeed:270, engine: '798 cc', price: '€11.990', mimages: '/static/images/mvAgustaF3800R.jpg', mrearImg: '/static/rearimg/mvAgustaF3800R-rear.jpg' , consumption: { value:6.2, unit: 'L/100km' }},

  { id: 'BRUTALE 800 R 35', name: '2025 MV Agusta BRUTALE 800 R 35', power:48, acc:3.3, topSpeed:240, engine: '798 cc', price: '€12.150', mimages: '/static/images/mvAgustaBRUTALE800R35.png', mrearImg: '/static/rearimg/mvAgustaBRUTALE800R35-rear.png' , consumption: { value:6.8, unit: 'L/100km' }},

  { id: 'PM-01 125',        name: '2025 Peugeot PM-01 125', power:15, acc:15, topSpeed:110, engine: '125 cc', price: '€3.590', mimages: '/static/images/peugeotPM-01125.png', mrearImg: '/static/rearimg/peugeotPM-01125-rear.png' , consumption: { value:2.5, unit: 'L/100km' }},

  { id: 'XP 400 GT',       name: '2025 Peugeot XP 400 GT', power:37, acc:135, topSpeed:137, engine: '400 cc', price: '€7.500', mimages: '/static/images/peugeotXP400GT.png', mrearImg: '/static/rearimg/peugeotXP400GT-rear.png' , consumption: { value:3.8, unit: 'L/100km' }},

  { id: 'SRT 900',         name: '2025 QJ Motor SRT 900', power:95, acc:4.5, topSpeed:190, engine: '900 cc', price: '€9.999', mimages: '/static/images/qjMotorSRT900.png', mrearImg: '/static/rearimg/qjMotorSRT900-rear.png' , consumption: { value:5.4, unit: 'L/100km' }},

  { id: 'SRK 600 RS',      name: '2025 QJ Motor SRK 600 RS', power:56, acc:4.5, topSpeed:190, engine: '600 cc', price: '€6.399', mimages: '/static/images/qjMotorSRK600RS.png', mrearImg: '/static/rearimg/qjMotorSRK600RS-rear.png' , consumption: { value:4.8, unit: 'L/100km' }},

  { id: 'SRK 921 RR',     name: '2025 QJ Motor SRK 921 RR', power:125, acc:3.3, topSpeed:245, engine: '921 cc', price: '€12.999', mimages: '/static/images/qjMotorSRK921RR.png', mrearImg: '/static/rearimg/qjMotorSRK921RR-rear.png' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: 'SRT 600 SX',      name: '2025 QJ Motor SRT 600 SX', power:56, acc:5.1, topSpeed:170, engine: '554 cc', price: '€5.799', mimages: '/static/images/qjMotorSRT600SX.png', mrearImg: '/static/rearimg/qjMotorSRT600SX-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},
  
  { id: 'Classic 650',     name: '2025 Royal Enfield Classic 650', power:48, acc:6.2, topSpeed:170, engine: '648 cc', price: '€7.380', mimages: '/static/images/royalEnfieldClassic650.png', mrearImg: '/static/rearimg/royalEnfieldClassic650-rear.png' , consumption: { value:4.7, unit: 'L/100km' }},

  { id: '300 SEF',         name: '2024 Sherco 300 SEF', power:24, acc:4.5, topSpeed:115, engine: '293 cc', price: '€8.999', mimages: '/static/images/sherco300SEF.png', mrearImg: '/static/rearimg/sherco300SEF-rear.png' , consumption: { value:3.2, unit: 'L/100km' }},

  { id: 'Varg EX',         name: '2025 Stark Varg EX', power:60, acc:5.0, topSpeed:120, engine: '900 Nm', price: '€12.990', mimages: '/static/images/starkVargEX.jpg', mrearImg: '/static/rearimg/starkVargEX-rear.jpg' , consumption: { value:6.0, unit: 'kWh/100km' }},

  { id: 'GSX-S 1000 F',    name: '2016 Suzuki GSX-S 1000 F', power:145, acc:3.3, topSpeed:250, engine: '999 cc', price: '€8.290', mimages: '/static/images/suzukiGSX-S1000F.png', mrearImg: '/static/rearimg/suzukiGSX-S1000F-rear.png' , consumption: { value:5.8, unit: 'L/100km' }},

  { id: 'DL 800',          name: '2023 Suzuki DL 800', power:84, acc:4.0, topSpeed:200, engine: '776 cc', price: '€8.990', mimages: '/static/images/suzukiDL800.png', mrearImg: '/static/rearimg/suzukiDL800-rear.png' , consumption: { value:4.6, unit: 'L/100km' }},

  { id: 'GSX-8R',          name: '2024 Suzuki GSX-8R', power:48, acc:3.7, topSpeed:215, engine: '776 cc', price: '€8.290', mimages: '/static/images/suzukiGSX-8R.png', mrearImg: '/static/rearimg/suzukiGSX-8R-rear.png' , consumption: { value:4.8, unit: 'L/100km' }},

  { id: 'GSX 8 S',         name: '2025 Suzuki GSX 8 S', power:48, acc:5.0, topSpeed:165, engine: '776 cc', price: '€7.289', mimages: '/static/images/suzukiGSX8S.png', mrearImg: '/static/rearimg/suzukiGSX8S-rear.png' , consumption: { value:4.7, unit: 'L/100km' }},

  { id: 'DL 650',          name: '2021 Suzuki DL 650', power:67, acc:4.0, topSpeed:185, engine: '645 cc', price: '€6.979', mimages: '/static/images/suzukiDL650.png', mrearImg: '/static/rearimg/suzukiDL650-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: 'GSX-1300 R HAYABUSA',   name: '2021 Suzuki GSX-1300 R HAYABUSA', power:190, acc:2.8, topSpeed:299, engine: '1340 cc', price: '€14.990', mimages: '/static/images/suzukiGSX-1300R-HAYABUSA.jpg', mrearImg: '/static/rearimg/suzukiGSX-1300R-HAYABUSA-rear.png' , consumption: { value:7.0, unit: 'L/100km' }},

  { id: 'M 1800 VZR',      name: '2015 Suzuki M 1800 VZR', power:125, acc:3.3, topSpeed:225, engine: '1783 cc', price: '€13.999', mimages: '/static/images/suzukiM1800VZR.jpg', mrearImg: '/static/rearimg/suzukiM1800VZR-rear.jpg' , consumption: { value:6.8, unit: 'L/100km' }},

  { id: 'Tiger 900 GT',    name: '2023 Triumph Tiger 900 GT', power:95, acc:3.9, topSpeed:205, engine: '888 cc', price: '€10.890', mimages: '/static/images/triumphTiger900GT.jpg', mrearImg: '/static/rearimg/triumphTiger900GT-rear.png' , consumption: { value:4.9, unit: 'L/100km' }},

  { id: 'STREET TRIPLE 765 RS',  name: '2021 Triumph STREET TRIPLE 765 RS', power:122, acc:3.0, topSpeed:245, engine: '765 cc', price: '€9.489', mimages: '/static/images/triumphSTREETTRIPLE765RS.jpg', mrearImg: '/static/rearimg/triumphSTREETTRIPLE765RS-rear.png' , consumption: { value:5.3, unit: 'L/100km' }},

  { id: 'Tiger Sport 800', name: '2025 Triumph Tiger Sport 800', power:114, acc:3.7, topSpeed:219, engine: '798 cc', price: '€10.390', mimages: '/static/images/triumphTigerSport800.jpg', mrearImg: '/static/rearimg/triumphTigerSport800-rear.png' , consumption: { value:5.0, unit: 'L/100km' }},

  { id: 'Gunner',          name: '2015 VICTORY Gunner', power:88, acc:5.0, topSpeed:200, engine: '1.731 cc', price: '€11.975', mimages: '/static/images/VICTORYGunner.png', mrearImg: '/static/rearimg/VICTORYGunner-rear.png' , consumption: { value:6.5, unit: 'L/100km' }},

  { id: 'DS 625 X',        name: '2025 VOGE DS 625 X', power:64, acc:4.5, topSpeed:185, engine: '581 cc', price: '€6.999', mimages: '/static/images/VOGEDS625X.png', mrearImg: '/static/rearimg/VOGEDS625X-rear.png' , consumption: { value:4.3, unit: 'L/100km' }},

  { id: 'R125',            name: '2025 VOGE R125 ABS', power:15, acc:15.0, topSpeed:120, engine: '124 cc', price: '€3.599', mimages: '/static/images/VOGER125.png', mrearImg: '/static/rearimg/VOGER125-rear.png' , consumption: { value:2.7, unit: 'L/100km' }},

  { id: 'YZF-R1 Termignoni',  name: '2014 Yamaha YZF-R1 Termignoni', power:182, acc:2.8, topSpeed:299, engine: '998 cc', price: '€12.450', mimages: '/static/images/yamahaYZFR1Termignoni.jpg', mrearImg: '/static/rearimg/yamahaYZFR1Termignoni-rear.png' , consumption: { value:6.7, unit: 'L/100km' }},

  { id: 'MT-07 IXIL',      name: '2018 Yamaha MT-07 IXIL', power:48, acc:4.5, topSpeed:180, engine: '689 cc', price: '€6.900', mimages: '/static/images/yamahaMT07IXIL.jpg', mrearImg: '/static/rearimg/yamahaMT07IXIL-rear.jpg' , consumption: { value:4.3, unit: 'L/100km' }},

  { id: 'YZF R1 60TH ANNIVERSARY',  name: '2023 Yamaha YZF R1 60TH ANNIVERSARY', power:200, acc:2.6, topSpeed:299, engine: '998 cc', price: '€23.489', mimages: '/static/images/yamahaYZFR160THANNIVERSARY.jpg', mrearImg: '/static/rearimg/yamahaYZFR160THANNIVERSARY-rear.png' , consumption: { value:6.8, unit: 'L/100km' }},

  { id: 'DSR',             name: '2025 Zero DSR', power:49, acc:3.4, topSpeed:180, engine: '229 Nm', price: '€20.500', mimages: '/static/images/ZeroDSR.jpg', mrearImg: '/static/rearimg/ZeroDSR-rear.png' , consumption: { value:8.0, unit: 'kWh/100km' }},

  { id: 'SR 15.6',         name: '2022 Zero SR 15.6', power:54, acc:4.0, topSpeed:145, engine: '40 kW', price: '€10.795 ', mimages: '/static/images/ZeroSR15.6.jpg', mrearImg: '/static/rearimg/ZeroSR15.6-rear.jpg' , consumption: { value:7.4, unit: 'kWh/100km' }},

  { id: 'SR',              name: '2021 Zero SR', power:54, acc:3.3, topSpeed:200, engine: '18 kWh', price: '€13.395', mimages: '/static/images/ZeroSR.png', mrearImg: '/static/rearimg/ZeroSR-rear.png' , consumption: { value:8.5, unit: 'kWh/100km' }},

  { id: '703 F',           name: '2025 Zontes 703 F', power:95, acc:4.3, topSpeed:200, engine: '699 cc', price: '€8.770', mimages: '/static/images/Zontes703F.png', mrearImg: '/static/rearimg/Zontes703F-rear.png' , consumption: { value:4.5, unit: 'L/100km' }},

  { id: 'ZT350',           name: '2022 Zontes ZT350', power:39, acc:5.5, topSpeed:145, engine: '348 cc', price: '€4.690', mimages: '/static/images/ZontesZT350.jpg', mrearImg: '/static/rearimg/ZontesZT350-rear.jpg' , consumption: { value:3.8, unit: 'L/100km' }},

  { id: ' 125 U',          name: '2026 Zontes 125 U', power:15, acc:14.0, topSpeed:117, engine: '124 cc', price: '€3.595', mimages: '/static/images/Zontes125U.png', mrearImg: '/static/rearimg/Zontes125U-rear.png' , consumption: { value:2.6, unit: 'L/100km' }},

  { id: 'ZT 703 RR',       name: '2026 Zontes ZT 703 RR', power:95, acc:3.8, topSpeed:210, engine: '699 cc', price: '€8.270', mimages: '/static/images/ZontesZT703RR.jpg', mrearImg: '/static/rearimg/ZontesZT703RR-rear.png' , consumption: { value:4.9, unit: 'L/100km' }}


];


globalThis.Motorcycles = Motorcycles;
globalThis.MOTORCYCLES_DATA = Motorcycles;
const MOTORCYCLES = Array.isArray(globalThis?.Motorcycles) ? globalThis.Motorcycles : Motorcycles;

const listEl = document.getElementById('itemList');
const compareArea = document.getElementById('compareArea');
const compareDecisionArea = document.getElementById('compareDecisionArea');
const compareDecisionVerdicts = document.getElementById('compareDecisionVerdicts');
const compareDecisionTradeoffs = document.getElementById('compareDecisionTradeoffs');
const compTable = document.querySelector('#compTable tbody');
const tableArea = document.getElementById('tableArea');
const raceLinksArea = document.getElementById('raceLinksArea');
const raceLinksList = document.getElementById('raceLinksList');
const searchInput = document.getElementById('search');
const brandSelect = document.getElementById('brandFilter');
const brandSymbolBar = document.getElementById('brandSymbolBar');
const clearBtn = document.getElementById('clearBtn');
const compareBtn = document.getElementById('compareBtn');
const fuelCalcSection = document.getElementById('fuelCalculator');
const fuelCalcDistance = document.getElementById('fuelCalcDistance');
const fuelCalcPrice = document.getElementById('fuelCalcPrice');
const fuelCalcUnit = document.getElementById('fuelCalcUnit');
const fuelCalcConsumption = document.getElementById('fuelCalcConsumption');
const fuelCalcResult = document.getElementById('fuelCalcResult');
const fuelCard = fuelCalcSection ? fuelCalcSection.querySelector('.fuel-card') : null;
const fuelPremiumLock = document.getElementById('fuelPremiumLock');
const fuelPremiumLockText = document.getElementById('fuelPremiumLockText');
const fuelPremiumUnlockBtn = document.getElementById('fuelPremiumUnlockBtn');
const fuelPremiumBadge = document.getElementById('fuelPremiumBadge');
const catalogToggle = document.getElementById('catalogToggle');
const catalogButtons = catalogToggle ? Array.from(catalogToggle.querySelectorAll('button[data-catalog]')) : [];
const topbarEl = document.querySelector('.topbar');
const authArea = document.querySelector('.auth-area');
const topFavoritesLink = document.getElementById('topFavoritesLink');
const favoritesAreaEl = document.getElementById('favoritesArea');
const favoritesListEl = document.getElementById('favoritesList');
const clearFavoritesBtn = document.getElementById('clearFavoritesBtn');
const notificationsBtn = document.getElementById('notificationsBtn');
const notificationsBadge = document.getElementById('notificationsBadge');
const notificationsMenu = document.getElementById('notificationsMenu');
const notificationsList = document.getElementById('notificationsList');
const TINY_IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';
let listLazyObserver = null;
const MIN_EAGER_LIST_IMAGES = 12;

function loadDeferredImage(img) {
  if (!img) return;
  const src = img.dataset.src;
  if (!src) return;
  img.src = src;
  img.removeAttribute('data-src');
}

function getInitialListImageCount() {
  const visibleHeight = listEl?.clientHeight || Math.round(window.innerHeight * 0.75);
  const estimatedRowHeight = 92;
  return Math.max(MIN_EAGER_LIST_IMAGES, Math.ceil(visibleHeight / estimatedRowHeight) + 6);
}

// language + translations
const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'tr', label: 'Türkçe' },
  { code: 'de', label: 'Deutsch' },
  { code: 'fr', label: 'Français' },
  { code: 'es', label: 'Español' },
];

const TRANSLATIONS = {
  en: {
    vehiclesTitle: 'Vehicles',
    motorcyclesTitle: 'Motorcycles',
    catalogCars: 'Cars',
    catalogMotorcycles: 'Motorcycles',
    searchPlaceholder: 'Search (model or brand)...',
    brandLabel: 'Brand',
    brandAll: 'All brands',
    filters: { topSpeed: 'Top Speed', nameAZ: 'A-Z', acc: '0-100 (s)', price: 'Price' },
    comparison: 'Comparison',
    clear: 'Clear Selected',
    compare: 'Compare',
    empty: 'No vehicles selected. Start by adding vehicles from the list.',
    add: 'Add',
    remove: 'Remove',
    details: 'Details',
    tableTitle: 'Comparison Table',
    tableHeaders: ['Model','Power (CV)','0-100 (s)','Top Speed (km/h)','Engine','Price','Consumption','Cost'],
    priceLabel: 'Price:',
    zeroToHundred: '0-100:',
    selectPrompt: 'Select at least one vehicle to compare',
    maxCompare: 'Maximum 5 vehicles for comparison. Premium: 8.',
    maxComparePremium: 'Maximum 8 vehicles for comparison',
    commentsTitle: 'Comments',
    commentName: 'Your name',
    commentPlaceholder: 'Write your comment...',
    ratingLabel: 'Rating:',
    submit: 'Submit',
    login: 'Log In',
    darkMode: 'Dark Mode',
    loginToComment: 'Please log in to comment.',
    costTitle: 'Cost of Ownership',
    consumptionLabel: 'Consumption',
    distanceLabel: 'Distance (km)',
    pricePerLiter: 'Price per L',
    pricePerKwh: 'Price per kWh',
    unitLabel: 'Unit',
    unitFuel: 'Fuel (L/100km)',
    unitElectric: 'Electric (kWh/100km)',
    costEstimate: 'Estimated cost',
    premiumBadge: 'Premium',
    premiumCostLocked: 'Cost of Ownership is a premium feature.',
    premiumUnlock: 'Upgrade to Unlock',
    premiumCheckoutLoading: 'Redirecting...',
    premiumCheckoutResume: 'Continue to Payment',
    premiumCheckoutError: 'Checkout could not be started. Please try again.',
    resaleButton: 'Resale',
    resaleTitle: 'Resale Value (5-10-15y)',
    resaleDepreciation: 'Depreciation',
    resaleAppreciation: 'Appreciation',
    resaleCollector: 'Collector',
    resaleLocked: 'Resale value is a premium feature.',
    resaleCategoryEconomy: 'Economy',
    resaleCategoryPremium: 'Premium',
    resaleCategoryLuxury: 'Luxury',
    resaleCategorySupercar: 'Supercar',
    resaleYear5: '5y',
    resaleYear10: '10y',
    resaleYear15: '15y',
    consumptionMissing: 'Consumption data not available',
    favoritesEmpty: 'No favorites yet.',
    addFavorite: 'Add to favorites',
    removeFavorite: 'Remove from favorites',
    navContact: 'Contact',
    navAbout: 'About Us',
    navPrivacy: 'Privacy Policy',
    navPricing: 'Pricing',
    navTerms: 'Terms',
    navRefund: 'Refund Policy',
    emptyNote: 'Prices reflect estimated market values and may vary by region.',
    seoHeading1: 'Car Performance & Cost Comparison Platform',
    seoP1: 'CarQuantix allows users to compare horsepower, acceleration, top speed and fuel consumption across multiple model years. Discover the best value per HP cars and performance rankings instantly.',
    seoHeading2: 'Car Fuel Cost Calculator',
    seoP2: 'With CarQuantix, you can easily calculate your vehicle\'s fuel consumption, cost per kilometer, and monthly fuel expenses. Compare gasoline, diesel, and electric vehicles based on real fuel prices.',
    seoHeading3: 'Cost Per Kilometer Calculation',
    seoP3: 'Enter your vehicle\'s fuel consumption (per 100 km) and current fuel price to instantly see your cost per kilometer, monthly, and yearly expenses.',
    seoHeading4: 'Electric Vehicle Charging Cost',
    seoP4: 'Calculate charging costs for electric vehicles using kWh/100km consumption values. Get detailed cost analysis based on current electricity prices.',
    seoHeading5: 'Popular Fuel Cost Pages',
    seoHeading6: 'Popular Performance & Top Speed',
    seoHeading7: 'Popular Comparisons',
  },
  tr: {
    vehiclesTitle: 'Araçlar',
    motorcyclesTitle: 'Motosikletler',
    catalogCars: 'Arabalar',
    catalogMotorcycles: 'Motosikletler',
    searchPlaceholder: 'Ara (model veya marka)...',
    brandLabel: 'Marka',
    brandAll: 'Tüm markalar',
    filters: { topSpeed: 'En yüksek hız', nameAZ: 'A-Z', acc: '0-100 (sn)', price: 'Fiyat' },
    comparison: 'Karşılaştırma',
    clear: 'Seçilenleri Temizle',
    compare: 'Karşılaştır',
    empty: 'Araç seçilmedi. Listeden ekleyin.',
    add: 'Ekle',
    remove: 'Kaldır',
    details: 'Detay',
    tableTitle: 'Karşılaştırma Tablosu',
    tableHeaders: ['Model','Güç (BG)','0-100 (sn)','Azami Hız (km/sa)','Motor','Fiyat','Tüketim','Maliyet'],
    priceLabel: 'Fiyat:',
    zeroToHundred: '0-100:',
    selectPrompt: 'Karşılaştırmak için en az bir araç seçin',
    maxCompare: 'En fazla 5 araç seçebilirsiniz. Premium: 8.',
    maxComparePremium: 'En fazla 8 araç seçebilirsiniz',
    commentsTitle: 'Yorumlar',
    commentName: 'Adınız',
    commentPlaceholder: 'Yorumunuzu yazın...',
    ratingLabel: 'Puan:',
    submit: 'Gönder',
    login: 'Giriş',
    darkMode: 'Karanlık Mod',
    loginToComment: 'Yorum yapmak için giriş yapın.',
    costTitle: 'Maliyet Hesaplayıcı',
    consumptionLabel: 'Tüketim',
    distanceLabel: 'Mesafe (km)',
    pricePerLiter: 'Litre fiyatı',
    pricePerKwh: 'kWh fiyatı',
    unitLabel: 'Birim',
    unitFuel: 'Yakıt (L/100km)',
    unitElectric: 'Elektrik (kWh/100km)',
    costEstimate: 'Tahmini maliyet',
    premiumBadge: 'Premium',
    premiumCostLocked: 'Sahip olma maliyeti premium özelliktir.',
    premiumUnlock: 'Yükselt ve Kilidi Aç',
    premiumCheckoutLoading: 'Yönlendiriliyor...',
    premiumCheckoutResume: 'Ödemeye Devam Et',
    premiumCheckoutError: 'Ödeme ekranı başlatılamadı. Lütfen tekrar deneyin.',
    resaleButton: 'Yeniden Satış',
    resaleTitle: 'Yeniden Satış Tahmini (5-10-15y)',
    resaleDepreciation: 'Değer Kaybı',
    resaleAppreciation: 'Değer Artışı',
    resaleCollector: 'Koleksiyon',
    resaleLocked: 'Yeniden satış tahmini premium özelliktir.',
    resaleCategoryEconomy: 'Ekonomi',
    resaleCategoryPremium: 'Premium',
    resaleCategoryLuxury: 'Lüks',
    resaleCategorySupercar: 'Süper',
    resaleYear5: '5 yıl',
    resaleYear10: '10 yıl',
    resaleYear15: '15 yıl',
    consumptionMissing: 'Tüketim verisi yok',
    favoritesEmpty: 'Henüz favori yok.',
    addFavorite: 'Favorilere ekle',
    removeFavorite: 'Favorilerden çıkar',
    navContact: 'İletişim',
    navAbout: 'Hakkımızda',
    navPrivacy: 'Gizlilik Politikası',
    navPricing: 'Fiyatlandirma',
    navTerms: 'Kosullar',
    navRefund: 'Iade Politikasi',
    emptyNote: 'Fiyatlar tahmini piyasa degerleridir; bolgeye gore degisebilir.',
    seoHeading1: 'Araç Performans & Maliyet Karşılaştırma Platformu',
    seoP1: 'CarQuantix, farklı model yıllarında beygir gücü, hızlanma, azami hız ve yakıt tüketimini karşılaştırmanı sağlar. En iyi fiyat/performans araçlarını hızlıca keşfet.',
    seoHeading2: 'Yakıt Maliyet Hesaplayıcı',
    seoP2: 'CarQuantix ile aracının yakıt tüketimini, km başı maliyeti ve aylık yakıt giderlerini kolayca hesaplayabilirsin. Benzin, dizel ve elektrikli araçları gerçek yakıt fiyatlarıyla karşılaştır.',
    seoHeading3: 'Kilometre Başına Maliyet',
    seoP3: '100 km başına tüketim ve güncel yakıt fiyatını girerek km, aylık ve yıllık maliyetini anında gör.',
    seoHeading4: 'Elektrikli Araç Şarj Maliyeti',
    seoP4: 'kWh/100km tüketim değerleri ile elektrikli araç şarj maliyetini hesapla. Güncel elektrik fiyatlarına göre detaylı analiz al.',
    seoHeading5: 'Popüler Yakıt Maliyet Sayfaları',
    seoHeading6: 'Popüler Performans & Azami Hız',
    seoHeading7: 'Popüler Karşılaştırmalar',
  },
  de: {
    vehiclesTitle: 'Fahrzeuge',
    searchPlaceholder: 'Suche (Modell oder Marke)...',
    brandLabel: 'Marke',
    brandAll: 'Alle Marken',
    filters: { topSpeed: 'Höchstgeschwindigkeit', nameAZ: 'A-Z', acc: '0-100 (s)', price: 'Preis' },
    comparison: 'Vergleich',
    clear: 'Auswahl löschen',
    compare: 'Vergleichen',
    empty: 'Keine Fahrzeuge gewählt. Füge welche aus der Liste hinzu.',
    add: 'Hinzufügen',
    remove: 'Entfernen',
    details: 'Details',
    tableTitle: 'Vergleichstabelle',
    tableHeaders: ['Modell','Leistung (PS)','0-100 (s)','Vmax (km/h)','Motor','Preis','Verbrauch','Kosten'],
    priceLabel: 'Preis:',
    zeroToHundred: '0-100:',
    selectPrompt: 'Wähle mindestens ein Fahrzeug zum Vergleichen',
    maxCompare: 'Maximal 5 Fahrzeuge. Premium: 8.',
    maxComparePremium: 'Maximal 8 Fahrzeuge',
    commentsTitle: 'Kommentare',
    commentName: 'Ihr Name',
    commentPlaceholder: 'Kommentar schreiben...',
    ratingLabel: 'Bewertung:',
    submit: 'Senden',
    login: 'Anmelden',
    darkMode: 'Dunkelmodus',
    loginToComment: 'Bitte anmelden, um zu kommentieren.',
    costTitle: 'Betriebskosten',
    consumptionLabel: 'Verbrauch',
    distanceLabel: 'Distanz (km)',
    pricePerLiter: 'Preis pro L',
    pricePerKwh: 'Preis pro kWh',
    unitLabel: 'Einheit',
    unitFuel: 'Kraftstoff (L/100km)',
    unitElectric: 'Strom (kWh/100km)',
    costEstimate: 'Kosten',
    consumptionMissing: 'Keine Verbrauchsdaten',
    favoritesEmpty: 'Noch keine Favoriten.',
    addFavorite: 'Zu Favoriten hinzufügen',
    removeFavorite: 'Aus Favoriten entfernen',
    navContact: 'Kontakt',
    navAbout: 'Uber uns',
    navPrivacy: 'Datenschutz',
    navPricing: 'Preise',
    navTerms: 'Bedingungen',
    navRefund: 'Rueckerstattung',
    emptyNote: 'Die Preise sind geschatzte Marktwerte und konnen je nach Region variieren.',
    seoHeading1: 'Plattform fur Leistungs- & Kostenvergleich',
    seoP1: 'CarQuantix vergleicht PS, Beschleunigung, Top Speed und Verbrauch uber mehrere Modelljahre. Finde schnell das beste Preis/Leistungs-Verhaltnis.',
    seoHeading2: 'Kraftstoffkosten-Rechner',
    seoP2: 'Mit CarQuantix kannst du Verbrauch, Kosten pro Kilometer und monatliche Ausgaben berechnen. Vergleiche Benzin, Diesel und Elektrofahrzeuge mit realen Preisen.',
    seoHeading3: 'Kosten pro Kilometer',
    seoP3: 'Gib den Verbrauch (pro 100 km) und den aktuellen Kraftstoffpreis ein, um Kosten pro km, monatlich und jahrlich zu sehen.',
    seoHeading4: 'Ladekosten fur Elektroautos',
    seoP4: 'Berechne Ladekosten mit kWh/100km Werten und erhalte eine Analyse basierend auf Strompreisen.',
    seoHeading5: 'Beliebte Kraftstoffkosten-Seiten',
    seoHeading6: 'Beliebte Performance & Top Speed',
    seoHeading7: 'Beliebte Vergleiche',
  },
  fr: {
    vehiclesTitle: 'Véhicules',
    searchPlaceholder: 'Rechercher (modèle ou marque)...',
    brandLabel: 'Marque',
    brandAll: 'Toutes les marques',
    filters: { topSpeed: 'Vitesse max', nameAZ: 'A-Z', acc: '0-100 (s)', price: 'Prix' },
    comparison: 'Comparaison',
    clear: 'Effacer la sélection',
    compare: 'Comparer',
    empty: 'Aucun véhicule sélectionné. Ajoutez-en depuis la liste.',
    add: 'Ajouter',
    remove: 'Retirer',
    details: 'Details',
    tableTitle: 'Tableau comparatif',
    tableHeaders: ['Modèle','Puissance (ch)','0-100 (s)','Vitesse max (km/h)','Moteur','Prix','Consommation','Coût'],
    priceLabel: 'Prix :',
    zeroToHundred: '0-100 :',
    selectPrompt: 'Sélectionnez au moins un véhicule pour comparer',
    maxCompare: 'Maximum 5 véhicules. Premium : 8.',
    maxComparePremium: 'Maximum 8 véhicules',
    commentsTitle: 'Commentaires',
    commentName: 'Votre nom',
    commentPlaceholder: 'Écrivez votre commentaire...',
    ratingLabel: 'Note :',
    submit: 'Envoyer',
    login: 'Connexion',
    darkMode: 'Mode sombre',
    loginToComment: 'Veuillez vous connecter pour commenter.',
    costTitle: 'Coût d’utilisation',
    consumptionLabel: 'Consommation',
    distanceLabel: 'Distance (km)',
    pricePerLiter: 'Prix par L',
    pricePerKwh: 'Prix par kWh',
    unitLabel: 'Unité',
    unitFuel: 'Carburant (L/100km)',
    unitElectric: 'Électrique (kWh/100km)',
    costEstimate: 'Coût estimé',
    consumptionMissing: 'Données de consommation indisponibles',
    favoritesEmpty: 'Aucun favori pour le moment.',
    addFavorite: 'Ajouter aux favoris',
    removeFavorite: 'Retirer des favoris',
    navContact: 'Contact',
    navAbout: 'A propos',
    navPrivacy: 'Politique de confidentialite',
    navPricing: 'Tarifs',
    navTerms: 'Conditions',
    navRefund: 'Politique de remboursement',
    emptyNote: 'Les prix sont des estimations du marche et peuvent varier selon la region.',
    seoHeading1: 'Plateforme de comparaison performance & cout',
    seoP1: 'CarQuantix compare puissance, acceleration, vitesse max et consommation sur plusieurs millesimes. Trouve rapidement le meilleur rapport prix/performances.',
    seoHeading2: 'Calculateur de cout carburant',
    seoP2: 'Avec CarQuantix, calcule la consommation, le cout par km et les depenses mensuelles. Compare essence, diesel et electrique avec des prix reels.',
    seoHeading3: 'Cout par kilometre',
    seoP3: 'Saisis la consommation (pour 100 km) et le prix actuel du carburant pour voir les couts par km, mensuels et annuels.',
    seoHeading4: 'Cout de recharge electrique',
    seoP4: 'Calcule les couts de recharge en kWh/100km et obtiens une analyse basee sur le prix de l\'electricite.',
    seoHeading5: 'Pages populaires de cout carburant',
    seoHeading6: 'Performances & Vitesse max populaires',
    seoHeading7: 'Comparaisons populaires',
  },
  es: {
    vehiclesTitle: 'Vehículos',
    searchPlaceholder: 'Buscar (modelo o marca)...',
    brandLabel: 'Marca',
    brandAll: 'Todas las marcas',
    filters: { topSpeed: 'Velocidad máx', nameAZ: 'A-Z', acc: '0-100 (s)', price: 'Precio' },
    comparison: 'Comparación',
    clear: 'Limpiar selección',
    compare: 'Comparar',
    empty: 'No hay vehículos seleccionados. Añade desde la lista.',
    add: 'Añadir',
    remove: 'Quitar',
    details: 'Detalles',
    tableTitle: 'Tabla comparativa',
    tableHeaders: ['Modelo','Potencia (CV)','0-100 (s)','Vel. máxima (km/h)','Motor','Precio','Consumo','Costo'],
    priceLabel: 'Precio:',
    zeroToHundred: '0-100:',
    selectPrompt: 'Selecciona al menos un vehículo para comparar',
    maxCompare: 'Máximo 5 vehículos. Premium: 8.',
    maxComparePremium: 'Máximo 8 vehículos',
    commentsTitle: 'Comentarios',
    commentName: 'Tu nombre',
    commentPlaceholder: 'Escribe tu comentario...',
    ratingLabel: 'Puntuación:',
    submit: 'Enviar',
    login: 'Iniciar sesión',
    darkMode: 'Modo oscuro',
    loginToComment: 'Inicia sesión para comentar.',
    costTitle: 'Costo de uso',
    consumptionLabel: 'Consumo',
    distanceLabel: 'Distancia (km)',
    pricePerLiter: 'Precio por L',
    pricePerKwh: 'Precio por kWh',
    unitLabel: 'Unidad',
    unitFuel: 'Combustible (L/100km)',
    unitElectric: 'Eléctrico (kWh/100km)',
    costEstimate: 'Costo estimado',
    consumptionMissing: 'Sin datos de consumo',
    favoritesEmpty: 'Aún no hay favoritos.',
    addFavorite: 'Añadir a favoritos',
    removeFavorite: 'Quitar de favoritos',
    navContact: 'Contacto',
    navAbout: 'Acerca de',
    navPrivacy: 'Politica de privacidad',
    navPricing: 'Precios',
    navTerms: 'Terminos',
    navRefund: 'Politica de reembolso',
    emptyNote: 'Los precios son estimaciones de mercado y pueden variar segun la region.',
    seoHeading1: 'Plataforma de comparacion de rendimiento y costo',
    seoP1: 'CarQuantix compara potencia, aceleracion, velocidad maxima y consumo entre varios años modelo. Descubre el mejor valor por HP al instante.',
    seoHeading2: 'Calculadora de costo de combustible',
    seoP2: 'Con CarQuantix puedes calcular consumo, costo por km y gastos mensuales. Compara gasolina, diesel y electricos con precios reales.',
    seoHeading3: 'Costo por kilometro',
    seoP3: 'Ingresa el consumo (por 100 km) y el precio actual del combustible para ver costos por km, mensuales y anuales.',
    seoHeading4: 'Costo de carga electrica',
    seoP4: 'Calcula costos de carga usando valores kWh/100km y obtiene un analisis basado en precios de electricidad.',
    seoHeading5: 'Paginas populares de costo de combustible',
    seoHeading6: 'Rendimiento y velocidad maxima populares',
    seoHeading7: 'Comparaciones populares',
  },
};

Object.assign(TRANSLATIONS.en, {
  navGuides: 'Guides',
  navBlog: 'Blog',
  navNews: 'News',
  notificationsTitle: 'Notifications',
  notificationsEmpty: 'No new vehicles yet.',
  notificationsNewArrival: 'New vehicle',
  notificationsCatalogCars: 'Car',
  notificationsCatalogMotorcycles: 'Motorcycle',
  notificationsToday: 'Today',
  notificationsYesterday: '1 day ago',
  notificationsDaysAgo: '{days} days ago',
});

Object.assign(TRANSLATIONS.tr, {
  navGuides: 'Rehberler',
  navBlog: 'Blog',
  navNews: 'Haberler',
  notificationsTitle: 'Bildirimler',
  notificationsEmpty: 'Henüz yeni araç yok.',
  notificationsNewArrival: 'Yeni araç',
  notificationsCatalogCars: 'Araba',
  notificationsCatalogMotorcycles: 'Motosiklet',
  notificationsToday: 'Bugün',
  notificationsYesterday: '1 gün önce',
  notificationsDaysAgo: '{days} gün önce',
});

Object.assign(TRANSLATIONS.de, {
  navGuides: 'Guides',
  navBlog: 'Blog',
  navNews: 'News',
  notificationsTitle: 'Benachrichtigungen',
  notificationsEmpty: 'Noch keine neuen Fahrzeuge.',
  notificationsNewArrival: 'Neues Fahrzeug',
  notificationsCatalogCars: 'Auto',
  notificationsCatalogMotorcycles: 'Motorrad',
  notificationsToday: 'Heute',
  notificationsYesterday: 'Vor 1 Tag',
  notificationsDaysAgo: 'Vor {days} Tagen',
});

Object.assign(TRANSLATIONS.fr, {
  navGuides: 'Guides',
  navBlog: 'Blog',
  navNews: 'Actualites',
  notificationsTitle: 'Notifications',
  notificationsEmpty: 'Aucun nouveau vehicule pour le moment.',
  notificationsNewArrival: 'Nouveau vehicule',
  notificationsCatalogCars: 'Voiture',
  notificationsCatalogMotorcycles: 'Moto',
  notificationsToday: 'Aujourd hui',
  notificationsYesterday: 'Il y a 1 jour',
  notificationsDaysAgo: 'Il y a {days} jours',
});

Object.assign(TRANSLATIONS.es, {
  navGuides: 'Guias',
  navBlog: 'Blog',
  navNews: 'Noticias',
  notificationsTitle: 'Notificaciones',
  notificationsEmpty: 'Aun no hay vehiculos nuevos.',
  notificationsNewArrival: 'Vehiculo nuevo',
  notificationsCatalogCars: 'Auto',
  notificationsCatalogMotorcycles: 'Motocicleta',
  notificationsToday: 'Hoy',
  notificationsYesterday: 'Hace 1 dia',
  notificationsDaysAgo: 'Hace {days} dias',
});

Object.assign(TRANSLATIONS.en, {
  raceLinksTitle: 'YouTube Race Links',
  raceLinksIntro: 'Open YouTube search results for head-to-head races of the selected vehicles.',
  raceLinksSearch: 'Search on YouTube',
});

Object.assign(TRANSLATIONS.tr, {
  raceLinksTitle: 'YouTube Yaris Linkleri',
  raceLinksIntro: 'Secili araclarin birebir yarislarini YouTube sonuc sayfasinda ac.',
  raceLinksSearch: 'YouTube\'da ara',
});

Object.assign(TRANSLATIONS.de, {
  raceLinksTitle: 'YouTube Rennlinks',
  raceLinksIntro: 'Offne YouTube-Suchergebnisse fur direkte Rennen der ausgewahlten Fahrzeuge.',
  raceLinksSearch: 'Auf YouTube suchen',
});

Object.assign(TRANSLATIONS.fr, {
  raceLinksTitle: 'Liens YouTube de course',
  raceLinksIntro: 'Ouvre les resultats YouTube pour des courses en face a face des vehicules selectionnes.',
  raceLinksSearch: 'Chercher sur YouTube',
});

Object.assign(TRANSLATIONS.es, {
  raceLinksTitle: 'Enlaces de carreras en YouTube',
  raceLinksIntro: 'Abre resultados de YouTube para carreras cara a cara de los vehiculos seleccionados.',
  raceLinksSearch: 'Buscar en YouTube',
});

const getLang = (code) => LANGUAGES.find(l => l.code === code);
let currentLang = localStorage.getItem('appLang');
if (!getLang(currentLang)) currentLang = LANGUAGES[0].code;

function getCurrencyForLang(code) {
  switch (code) {
    case 'tr':
      return 'TRY';
    case 'en':
      return 'USD';
    case 'de':
    case 'fr':
    case 'es':
    default:
      return 'EUR';
  }
}

const t = (key) => {
  const langPack = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  return langPack[key] || TRANSLATIONS.en[key] || key;
};

const HEART_FILLED = '&#9829;';
const HEART_EMPTY = '&#9825;';
let sessionUser = (window.currentUser && (window.currentUser.email || window.currentUser.name || window.currentUser.id || window.currentUser.sub)) ? window.currentUser : null;
function computePremiumAccess(user) {
  return Boolean(
    user && (
      user.is_premium === true
      || ['active', 'trialing'].includes(String(user.subscription_status || '').toLowerCase())
    )
  );
}
let hasPremiumAccess = computePremiumAccess(sessionUser);
const FREE_COMPARE_LIMIT = 5;
const PREMIUM_COMPARE_LIMIT = 8;
let compareLimit = hasPremiumAccess ? PREMIUM_COMPARE_LIMIT : FREE_COMPARE_LIMIT;
const sessionUserId = sessionUser
  ? (sessionUser.email || sessionUser.name || sessionUser.id || sessionUser.sub || sessionUser.user_id || 'user')
  : null;
const favoritesKey = sessionUserId ? `favorites:${sessionUserId}` : null;
const inventorySnapshotKey = sessionUserId ? `inventorySnapshot:${sessionUserId}` : null;
const inventoryNotificationsKey = sessionUserId ? `inventoryNotifications:${sessionUserId}` : null;
const favoritesEnabled = Boolean(sessionUserId && favoritesListEl);
const notificationsEnabled = Boolean(
  sessionUserId
  && notificationsBtn
  && notificationsBadge
  && notificationsMenu
  && notificationsList
);

function syncPremiumState(nextUser) {
  if (nextUser) {
    sessionUser = nextUser;
    window.currentUser = nextUser;
  }
  hasPremiumAccess = computePremiumAccess(sessionUser);
  compareLimit = hasPremiumAccess ? PREMIUM_COMPARE_LIMIT : FREE_COMPARE_LIMIT;
}

function unlockPremiumUi() {
  if (sessionUser) {
    syncPremiumState({
      ...sessionUser,
      is_premium: true,
      subscription_status: 'active',
    });
  } else {
    hasPremiumAccess = true;
    compareLimit = PREMIUM_COMPARE_LIMIT;
  }
  updateFuelPremiumUi();
  updateFuelCalculator();
  renderSelected();
  if (selected.length) buildTable();
}

function normalizeFavorites(list) {
  if (!Array.isArray(list)) return [];
  const seen = new Set();
  const normalized = [];
  list.forEach(entry => {
    if (!entry) return;
    const key = entry.key || (entry.catalog && entry.id ? makeKey(entry.catalog, entry.id) : null);
    if (!key || seen.has(key)) return;
    const parsed = parseKey(key);
    const catalog = parsed.catalog || entry.catalog || 'cars';
    const id = parsed.id || entry.id;
    if (!id) return;
    seen.add(key);
    normalized.push({ key, catalog, id, ts: entry.ts || Date.now() });
  });
  return normalized;
}

function loadFavorites() {
  if (!favoritesKey) return [];
  try {
    const raw = JSON.parse(localStorage.getItem(favoritesKey) || '[]');
    return normalizeFavorites(raw);
  } catch (err) {
    return [];
  }
}

function saveFavorites() {
  if (!favoritesKey) return;
  localStorage.setItem(favoritesKey, JSON.stringify(favorites));
}

function isFavorite(key) {
  return favorites.some(f => f.key === key);
}

function resolveFavoriteVehicle(fav) {
  const parsed = fav?.key ? parseKey(fav.key) : { catalog: fav.catalog, id: fav.id };
  const catalog = parsed.catalog || fav.catalog || 'cars';
  const id = String(parsed.id || fav.id || '');
  const source = catalog === 'motorcycles' ? MOTORCYCLES : VEHICLES;
  const veh = source.find(x => String(x.id) === id);
  return { veh, catalog, id, key: fav.key || makeKey(catalog, id) };
}

function toggleFavorite(key, catalog, id) {
  if (!favoritesEnabled) return;
  const exists = isFavorite(key);
  if (exists) {
    favorites = favorites.filter(f => f.key !== key);
  } else {
    favorites = [{ key, catalog, id, ts: Date.now() }, ...favorites];
  }
  saveFavorites();
  renderFavorites();
  updateListFavoriteButtons();
}

function updateListFavoriteButtons() {
  if (!favoritesEnabled || !listEl) return;
  listEl.querySelectorAll('.fav-btn').forEach(btn => {
    const key = btn.dataset.id;
    const active = isFavorite(key);
    btn.classList.toggle('active', active);
    btn.innerHTML = active ? HEART_FILLED : HEART_EMPTY;
    const label = active ? t('removeFavorite') : t('addFavorite');
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
  });
}

function attachListFavoriteButtons() {
  if (!favoritesEnabled || !listEl) return;
  listEl.querySelectorAll('.fav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parsed = parseKey(btn.dataset.id);
      const source = parsed.catalog === 'motorcycles' ? MOTORCYCLES : VEHICLES;
      const veh = source.find(x => String(x.id) === parsed.id);
      if (!veh) return;
      toggleFavorite(btn.dataset.id, parsed.catalog, parsed.id);
    });
  });
}

function renderFavorites() {
  if (!favoritesEnabled || !favoritesListEl) return;
  favoritesListEl.innerHTML = '';
  const resolved = [];
  favorites.forEach(f => {
    const { veh, catalog, id, key } = resolveFavoriteVehicle(f);
    if (!veh) return;
    resolved.push({ veh, catalog, id, key });
  });
  if (resolved.length !== favorites.length) {
    favorites = normalizeFavorites(resolved.map(r => ({ key: r.key, catalog: r.catalog, id: r.id })));
    saveFavorites();
  }
  if (!resolved.length) {
    favoritesListEl.innerHTML = `<div id="favoritesEmpty" class="empty-note">${t('favoritesEmpty')}</div>`;
    if (clearFavoritesBtn) clearFavoritesBtn.disabled = true;
    return;
  }
  if (clearFavoritesBtn) clearFavoritesBtn.disabled = false;
  resolved.forEach(({ veh, key, catalog, id }) => {
    const card = document.createElement('div');
    card.className = 'favorite-card';
    const thumb = safeImg(resolveMainImage(veh), veh.name);
    card.innerHTML = `
      <img class="thumb" src="${thumb}" alt="${veh.name}" loading="lazy" decoding="async" />
      <div class="info">
        <h3>${veh.name}</h3>
        <p>${veh.engine} Â· ${veh.power} CV Â· ${veh.topSpeed} km/h</p>
      </div>
      <div class="fav-actions">
        <button class="add-btn" data-id="${key}" aria-label="${t('add')} ${veh.name}">${t('add')}</button>
        <button class="fav-btn active" data-id="${key}" aria-label="${t('removeFavorite')}" title="${t('removeFavorite')}">${HEART_FILLED}</button>
      </div>
    `;
    favoritesListEl.appendChild(card);
  });
  favoritesListEl.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parsed = parseKey(btn.dataset.id);
      const source = parsed.catalog === 'motorcycles' ? MOTORCYCLES : VEHICLES;
      const veh = source.find(x => String(x.id) === parsed.id);
      if (!veh) return;
      const key = makeKey(parsed.catalog, parsed.id);
      if (selected.find(s => (s._key || makeKey(s.catalog || 'cars', s.id)) === key)) return;
      if (selected.length >= compareLimit) {
        alert(hasPremiumAccess ? t('maxComparePremium') : t('maxCompare'));
        return;
      }
      selected.push({ ...veh, _key: key, catalog: parsed.catalog });
      renderSelected();
    });
  });
  favoritesListEl.querySelectorAll('.fav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parsed = parseKey(btn.dataset.id);
      toggleFavorite(btn.dataset.id, parsed.catalog, parsed.id);
    });
  });
}

function initFavoritesUI() {
  if (!favoritesEnabled) return;
  if (topFavoritesLink && favoritesAreaEl) {
    const closeFavorites = () => {
      favoritesAreaEl.classList.remove('open');
      topFavoritesLink.setAttribute('aria-expanded', 'false');
    };
    topFavoritesLink.addEventListener('click', (e) => {
      e.preventDefault();
      const willOpen = !favoritesAreaEl.classList.contains('open');
      document.querySelectorAll('.favorites-popover.open').forEach(pop => pop.classList.remove('open'));
      favoritesAreaEl.classList.toggle('open', willOpen);
      topFavoritesLink.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });
    document.addEventListener('click', (e) => {
      if (!favoritesAreaEl.contains(e.target) && !topFavoritesLink.contains(e.target)) {
        closeFavorites();
      }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeFavorites();
    });
  }
  if (clearFavoritesBtn) {
    clearFavoritesBtn.addEventListener('click', () => {
      favorites = [];
      saveFavorites();
      renderFavorites();
      updateListFavoriteButtons();
    });
  }
}

let favorites = favoritesEnabled ? loadFavorites() : [];
let inventoryNotifications = notificationsEnabled ? loadInventoryNotifications() : [];

let selected = [];
let activeSort = null;
let activeCatalog = 'cars';
const brandSelectionByCatalog = {};
let activeBrand = 'all';
const INVENTORY_MAP = { cars: VEHICLES, motorcycles: MOTORCYCLES };
const MOBILE_SPLIT_QUERY = '(max-width: 760px)';
let mobileVehicleToggleBtn = null;
const savedCatalog = localStorage.getItem('catalogType');
if (savedCatalog && INVENTORY_MAP[savedCatalog]) {
  activeCatalog = savedCatalog;
}

function makeKey(catalog, id) {
  return `${catalog}:${encodeURIComponent(String(id ?? ''))}`;
}

function isMobileSplitLayout() {
  return typeof window !== 'undefined'
    && typeof window.matchMedia === 'function'
    && window.matchMedia(MOBILE_SPLIT_QUERY).matches;
}

function getVehiclePanelLabel() {
  const translated = t('vehiclesTitle');
  return translated && translated !== 'vehiclesTitle' ? translated : 'Vehicles';
}

function updateMobileVehicleToggle() {
  if (!mobileVehicleToggleBtn) return;
  const shouldShow = isMobileSplitLayout() && selected.length > 0;
  const isCollapsed = document.body.classList.contains('mobile-sidebar-collapsed');
  mobileVehicleToggleBtn.hidden = !shouldShow;
  mobileVehicleToggleBtn.classList.toggle('is-collapsed', isCollapsed);
  mobileVehicleToggleBtn.setAttribute('aria-expanded', String(!isCollapsed));
  mobileVehicleToggleBtn.innerHTML = `
    <span class="panel-toggle-icon">${isCollapsed ? '&#9776;' : '&times;'}</span>
    <span>${getVehiclePanelLabel()}</span>
  `;
}

function setMobileSidebarCollapsed(collapsed) {
  const shouldCollapse = Boolean(collapsed) && isMobileSplitLayout() && selected.length > 0;
  document.body.classList.toggle('mobile-sidebar-collapsed', shouldCollapse);
  updateMobileVehicleToggle();
}

function syncMobileViewportLayout() {
  if (typeof document === 'undefined') return;
  const topbarHeight = topbarEl ? Math.ceil(topbarEl.getBoundingClientRect().height) : 0;
  document.documentElement.style.setProperty('--mobile-topbar-height', `${topbarHeight}px`);
}

function parseKey(key) {
  const [catalog, ...rest] = String(key || '').split(':');
  return { catalog: catalog || 'cars', id: decodeURIComponent(rest.join(':') || '') };
}

const DAY_MS = 24 * 60 * 60 * 1000;
const NOTIFICATION_SEED_WINDOW_DAYS = 30;

function readStoredJson(key, fallback) {
  if (!key) return fallback;
  try {
    const parsed = JSON.parse(localStorage.getItem(key) || 'null');
    return parsed ?? fallback;
  } catch (err) {
    return fallback;
  }
}

function parseNoticeTimestamp(value) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (!value) return null;
  const parsed = Date.parse(String(value));
  return Number.isFinite(parsed) ? parsed : null;
}

function loadInventorySnapshot() {
  const snapshot = readStoredJson(inventorySnapshotKey, []);
  return Array.isArray(snapshot) ? snapshot.map(String) : [];
}

function saveInventorySnapshot(keys) {
  if (!inventorySnapshotKey) return;
  localStorage.setItem(inventorySnapshotKey, JSON.stringify(Array.from(new Set(keys.map(String)))));
}

function normalizeInventoryNotifications(list) {
  if (!Array.isArray(list)) return [];
  const seen = new Set();
  const normalized = [];
  list.forEach(entry => {
    if (!entry || !entry.key || seen.has(entry.key)) return;
    seen.add(entry.key);
    normalized.push({
      key: String(entry.key),
      read: Boolean(entry.read),
      detectedAt: parseNoticeTimestamp(entry.detectedAt) || Date.now(),
    });
  });
  return normalized;
}

function loadInventoryNotifications() {
  return normalizeInventoryNotifications(readStoredJson(inventoryNotificationsKey, []));
}

function saveInventoryNotifications() {
  if (!inventoryNotificationsKey) return;
  localStorage.setItem(inventoryNotificationsKey, JSON.stringify(inventoryNotifications));
}

function getInventoryNotificationFeed() {
  return [
    ...VEHICLES.map(vehicle => ({ catalog: 'cars', vehicle })),
    ...MOTORCYCLES.map(vehicle => ({ catalog: 'motorcycles', vehicle })),
  ];
}

function buildRecentArrivalNotifications(feed, existingKeys = new Set()) {
  const windowStart = Date.now() - (NOTIFICATION_SEED_WINDOW_DAYS * DAY_MS);
  return feed
    .filter(entry => {
      const key = makeKey(entry.catalog, entry.vehicle.id);
      const addedAt = parseNoticeTimestamp(entry.vehicle.addedAt);
      return addedAt && addedAt >= windowStart && !existingKeys.has(key);
    })
    .map(entry => ({
      key: makeKey(entry.catalog, entry.vehicle.id),
      detectedAt: parseNoticeTimestamp(entry.vehicle.addedAt) || Date.now(),
      read: false,
    }));
}

function resolveNotificationVehicle(notice) {
  const parsed = parseKey(notice?.key);
  const source = parsed.catalog === 'motorcycles' ? MOTORCYCLES : VEHICLES;
  const vehicle = source.find(item => String(item.id) === parsed.id);
  return { vehicle, catalog: parsed.catalog || 'cars' };
}

function getNotificationAgeLabel(timestamp) {
  const diff = Math.max(0, Date.now() - timestamp);
  const days = Math.floor(diff / DAY_MS);
  if (days <= 0) return t('notificationsToday');
  if (days === 1) return t('notificationsYesterday');
  return String(t('notificationsDaysAgo')).replace('{days}', String(days));
}

function updateNotificationsBadge() {
  if (!notificationsEnabled) return;
  const unreadCount = inventoryNotifications.filter(notice => !notice.read).length;
  notificationsBadge.textContent = unreadCount > 99 ? '99+' : String(unreadCount);
  notificationsBadge.classList.toggle('hidden', unreadCount === 0);
  notificationsBtn.classList.toggle('has-unread', unreadCount > 0);
  notificationsBtn.setAttribute('aria-expanded', notificationsMenu.classList.contains('open') ? 'true' : 'false');
}

function renderNotifications() {
  if (!notificationsEnabled) return;
  const titleEl = notificationsMenu.querySelector('.notifications-title');
  if (titleEl) titleEl.textContent = t('notificationsTitle');

  const activeKeys = new Set(getInventoryNotificationFeed().map(entry => makeKey(entry.catalog, entry.vehicle.id)));
  const nextNotifications = normalizeInventoryNotifications(
    inventoryNotifications.filter(notice => activeKeys.has(notice.key))
  );
  if (nextNotifications.length !== inventoryNotifications.length) {
    inventoryNotifications = nextNotifications;
    saveInventoryNotifications();
  }

  notificationsList.innerHTML = '';
  if (!inventoryNotifications.length) {
    notificationsList.innerHTML = `<div class="notice-empty">${t('notificationsEmpty')}</div>`;
    updateNotificationsBadge();
    return;
  }

  const sorted = [...inventoryNotifications].sort((left, right) => {
    const leftTs = parseNoticeTimestamp(resolveNotificationVehicle(left).vehicle?.addedAt) || left.detectedAt || 0;
    const rightTs = parseNoticeTimestamp(resolveNotificationVehicle(right).vehicle?.addedAt) || right.detectedAt || 0;
    return rightTs - leftTs;
  });

  sorted.forEach(notice => {
    const { vehicle, catalog } = resolveNotificationVehicle(notice);
    if (!vehicle) return;
    const itemTimestamp = parseNoticeTimestamp(vehicle.addedAt) || notice.detectedAt || Date.now();
    const catalogLabel = catalog === 'motorcycles'
      ? t('notificationsCatalogMotorcycles')
      : t('notificationsCatalogCars');
    const item = document.createElement('div');
    item.className = `notice-item${notice.read ? '' : ' is-unread'}`;
    item.innerHTML = `
      <div class="notice-kicker">${t('notificationsNewArrival')}</div>
      <div class="notice-text">${vehicle.name}</div>
      <div class="notice-date">${catalogLabel} · ${getNotificationAgeLabel(itemTimestamp)}</div>
    `;
    notificationsList.appendChild(item);
  });

  updateNotificationsBadge();
}

function markNotificationsRead() {
  if (!notificationsEnabled) return;
  let changed = false;
  inventoryNotifications = inventoryNotifications.map(notice => {
    if (notice.read) return notice;
    changed = true;
    return { ...notice, read: true };
  });
  if (changed) saveInventoryNotifications();
  renderNotifications();
}

function closeNotificationsMenu() {
  if (!notificationsEnabled) return;
  notificationsMenu.classList.remove('open');
  updateNotificationsBadge();
}

function syncInventoryNotifications() {
  if (!notificationsEnabled) return;
  const feed = getInventoryNotificationFeed();
  const currentKeys = feed.map(entry => makeKey(entry.catalog, entry.vehicle.id));
  inventoryNotifications = loadInventoryNotifications();
  const snapshot = loadInventorySnapshot();
  const existingNoticeKeys = new Set(inventoryNotifications.map(notice => notice.key));
  const seededRecentArrivals = buildRecentArrivalNotifications(feed, existingNoticeKeys);

  if (!snapshot.length) {
    inventoryNotifications = normalizeInventoryNotifications([
      ...seededRecentArrivals,
      ...inventoryNotifications,
    ]);
    saveInventorySnapshot(currentKeys);
    saveInventoryNotifications();
    renderNotifications();
    return;
  }

  const knownKeys = new Set(snapshot);
  const unseenArrivals = feed
    .filter(entry => !knownKeys.has(makeKey(entry.catalog, entry.vehicle.id)))
    .map(entry => ({
      key: makeKey(entry.catalog, entry.vehicle.id),
      detectedAt: parseNoticeTimestamp(entry.vehicle.addedAt) || Date.now(),
      read: false,
    }));

  const activeKeys = new Set(currentKeys);
  inventoryNotifications = normalizeInventoryNotifications([
    ...unseenArrivals,
    ...seededRecentArrivals,
    ...inventoryNotifications.filter(notice => activeKeys.has(notice.key)),
  ]);

  saveInventorySnapshot(currentKeys);
  saveInventoryNotifications();
  renderNotifications();
}

function initNotificationsUI() {
  if (!notificationsEnabled) return;
  syncInventoryNotifications();

  notificationsBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    const willOpen = !notificationsMenu.classList.contains('open');
    notificationsMenu.classList.toggle('open', willOpen);
    updateNotificationsBadge();
    if (willOpen) markNotificationsRead();
  });

  notificationsMenu.addEventListener('click', event => {
    event.stopPropagation();
  });

  document.addEventListener('click', event => {
    if (!notificationsMenu.contains(event.target) && !notificationsBtn.contains(event.target)) {
      closeNotificationsMenu();
    }
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeNotificationsMenu();
  });
}

function slugifyName(value) {
  const normalized = String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '');
  const slug = normalized
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
  return slug || 'car';
}

function buildCarDetailUrl(vehicle) {
  const name = vehicle?.name || vehicle?.id || '';
  return `/cars/${slugifyName(name)}`;
}

function currentInventory() {
  return INVENTORY_MAP[activeCatalog] || VEHICLES;
}

// util: safe image (use placeholder if image not present)
function safeImg(path, label){
  // If path looks like an external URL, return it directly
  if (/^(https?:)?\/\//.test(path)) return path;
  // Use placeholder if local image missing; browsers will still try to load local path
  return path || `https://via.placeholder.com/320x180?text=${encodeURIComponent(label)}`;
}

function normalizeMotoPath(path) {
  if (!path) return path;
  if (path.startsWith('/static/images/')) return path.replace('/static/images/', '/static/mimages/');
  if (path.startsWith('/static/rearimg/')) return path.replace('/static/rearimg/', '/static/mrearimg/');
  return path;
}

function resolveMainImage(v) {
  let src = v?.img || v?.image || v?.images || v?.mainImg || v?.mimages || '';
  if (v?.mimages || v?.mrearImg || v?.mrearimg) src = normalizeMotoPath(src);
  return src;
}

function resolveRearImage(v) {
  let src = v?.rearImg || v?.rearImage || v?.mrearImg || v?.mrearimg || v?.rear || '';
  if (v?.mimages || v?.mrearImg || v?.mrearimg) src = normalizeMotoPath(src);
  return src;
}

// decide fit mode based on aspect ratio
function applyFitMode(img){
  if (!img) return;
  img.classList.remove('fit-contain');
  img.classList.add('fit-cover');
}

function extractAverageColor(img) {
  try {
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    if (!w || !h) return null;
    const size = 24;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    canvas.width = size;
    canvas.height = size;
    ctx.drawImage(img, 0, 0, size, size);
    const data = ctx.getImageData(0, 0, size, size).data;
    let r = 0;
    let g = 0;
    let b = 0;
    let count = 0;
    for (let i = 0; i < data.length; i += 4) {
      const alpha = data[i + 3];
      if (alpha < 200) continue;
      r += data[i];
      g += data[i + 1];
      b += data[i + 2];
      count++;
    }
    if (!count) return null;
    r = Math.round(r / count);
    g = Math.round(g / count);
    b = Math.round(b / count);
    return { r, g, b };
  } catch (err) {
    return null;
  }
}

function applyCardAccent(card, img) {
  const avg = extractAverageColor(img);
  if (!avg) return;
  const lum = 0.2126 * avg.r + 0.7152 * avg.g + 0.0722 * avg.b;
  let r = avg.r;
  let g = avg.g;
  let b = avg.b;
  if (lum < 110) {
    r = Math.min(255, r + 100);
    g = Math.min(255, g + 100);
    b = Math.min(255, b + 100);
  } else if (lum > 210) {
    r = Math.max(0, r - 70);
    g = Math.max(0, g - 70);
    b = Math.max(0, b - 70);
  } else {
    r = Math.min(255, r + 35);
    g = Math.min(255, g + 35);
    b = Math.min(255, b + 35);
  }
  const strong = {
    r: Math.min(255, r + 20),
    g: Math.min(255, g + 20),
    b: Math.min(255, b + 20),
  };
  card.style.setProperty('--card-accent', `rgb(${r}, ${g}, ${b})`);
  card.style.setProperty('--card-accent-strong', `rgb(${strong.r}, ${strong.g}, ${strong.b})`);
  card.style.setProperty('--card-accent-soft', `rgba(${r}, ${g}, ${b}, 0.28)`);
}

// derive brand label from vehicle name
const MULTI_BRAND_PREFIXES = [
  'alfa romeo',
  'aston martin',
  'land rover',
  'range rover',
  'rolls royce',
  'mercedes-benz',
  'mercedes benz',
];

function getBrandLabel(name = '') {
  const cleaned = name.replace(/^\d{4}\s+/, '').trim();
  if (!cleaned) return 'Other';
  const lower = cleaned.toLowerCase();
  const multi = MULTI_BRAND_PREFIXES.find(prefix => lower.startsWith(prefix));
  if (multi) return cleaned.slice(0, multi.length);
  const first = cleaned.split(/\s+/)[0];
  return first || 'Other';
}

function createBrandDivider(label) {
  const divider = document.createElement('div');
  divider.className = 'brand-divider';
  divider.innerHTML = `<span>${label}</span>`;
  return divider;
}

function getBrandList() {
  const brands = new Set();
  currentInventory().forEach(v => {
    const brand = getBrandLabel(v.name);
    if (brand) brands.add(brand);
  });
  return Array.from(brands).sort((a, b) => a.localeCompare(b));
}

function hashBrand(label = '') {
  let hash = 0;
  for (let i = 0; i < label.length; i += 1) {
    hash = ((hash << 5) - hash) + label.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

function getBrandMonogram(label = '') {
  const parts = String(label || '')
    .replace(/[^a-z0-9\s-]/gi, ' ')
    .split(/[\s-]+/)
    .filter(Boolean);
  if (!parts.length) return '?';
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return parts.slice(0, 2).map(part => part[0]).join('').toUpperCase();
}

function buildBrandSymbolButtons(brands) {
  if (!brandSymbolBar) return;
  brandSymbolBar.innerHTML = '';

  const entries = [{ value: 'all', label: t('brandAll') }, ...brands.map(brand => ({ value: brand, label: brand }))];
  entries.forEach(entry => {
    const btn = document.createElement('button');
    const hue = entry.value === 'all' ? 205 : (hashBrand(entry.label) % 360);
    const isActive = (activeBrand || 'all') === entry.value;
    btn.type = 'button';
    btn.className = `brand-symbol-btn${isActive ? ' active' : ''}`;
    btn.dataset.brand = entry.value;
    btn.title = entry.label;
    btn.setAttribute('role', 'option');
    btn.setAttribute('aria-label', entry.label);
    btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
    btn.style.setProperty('--brand-hue', String(hue));
    btn.innerHTML = `<span class="brand-symbol-mark">${entry.value === 'all' ? 'ALL' : getBrandMonogram(entry.label)}</span>`;
    btn.addEventListener('click', () => {
      activeBrand = entry.value;
      brandSelectionByCatalog[activeCatalog] = activeBrand;
      if (brandSelect) brandSelect.value = activeBrand;
      buildBrandSymbolButtons(brands);
      renderList(searchInput ? searchInput.value : '');
    });
    brandSymbolBar.appendChild(btn);
  });
}

function buildBrandOptions() {
  if (!brandSelect) return;
  const brands = getBrandList();
  brandSelect.innerHTML = '';
  const allOption = document.createElement('option');
  allOption.value = 'all';
  allOption.textContent = t('brandAll');
  brandSelect.appendChild(allOption);
  brands.forEach(brand => {
    const option = document.createElement('option');
    option.value = brand;
    option.textContent = brand;
    brandSelect.appendChild(option);
  });
  const saved = brandSelectionByCatalog[activeCatalog] || activeBrand || 'all';
  activeBrand = brands.includes(saved) ? saved : 'all';
  brandSelect.value = activeBrand;
  buildBrandSymbolButtons(brands);
}

function parsePrice(val) {
  if (!val) return 0;
  const digits = String(val).replace(/\D/g, '');
  return Number(digits) || 0;
}

function getLocaleForLang(code) {
  switch (String(code || 'en').toLowerCase()) {
    case 'tr':
      return 'tr-TR';
    case 'de':
      return 'de-DE';
    case 'fr':
      return 'fr-FR';
    case 'es':
      return 'es-ES';
    case 'en':
    default:
      return 'en-US';
  }
}

function extractVehicleYear(name) {
  const match = String(name || '').match(/\b(19|20)\d{2}\b/);
  if (!match) return null;
  const year = Number(match[0]);
  return Number.isFinite(year) ? year : null;
}

const COLLECTOR_MAX_YEAR = 2005;
const COLLECTOR_MIN_PRICE = 150000;
const COLLECTOR_APPRECIATION_RATE = 0.04;
const RESALE_CATEGORIES = [
  { key: 'economy', min: 0, max: 20000, rate: 0.12 },
  { key: 'premium', min: 20000, max: 60000, rate: 0.10 },
  { key: 'luxury', min: 60000, max: 150000, rate: 0.15 },
  { key: 'supercar', min: 150000, max: Infinity, rate: 0.18 },
];

function getResaleCategory(price) {
  const value = Number(price) || 0;
  return RESALE_CATEGORIES.find(cat => value >= cat.min && value < cat.max) || RESALE_CATEGORIES[0];
}

function getResaleCategoryLabel(key) {
  switch (key) {
    case 'economy':
      return t('resaleCategoryEconomy');
    case 'premium':
      return t('resaleCategoryPremium');
    case 'luxury':
      return t('resaleCategoryLuxury');
    case 'supercar':
      return t('resaleCategorySupercar');
    default:
      return '';
  }
}

function buildResalePrediction(vehicle) {
  const price = parsePrice(vehicle?.price);
  if (!Number.isFinite(price) || price <= 0) return null;
  const year = extractVehicleYear(vehicle?.name);
  const isCollector = Boolean(year && year <= COLLECTOR_MAX_YEAR && price >= COLLECTOR_MIN_PRICE);
  if (isCollector) {
    return {
      kind: 'appreciation',
      rate: COLLECTOR_APPRECIATION_RATE,
      categoryLabel: t('resaleCollector'),
      values: [5, 10, 15].map(y => Math.round(price * Math.pow(1 + COLLECTOR_APPRECIATION_RATE, y))),
    };
  }
  const category = getResaleCategory(price);
  return {
    kind: 'depreciation',
    rate: category.rate,
    categoryLabel: getResaleCategoryLabel(category.key),
    values: [5, 10, 15].map(y => Math.round(price * Math.pow(1 - category.rate, y))),
  };
}

function formatRate(rate) {
  if (!Number.isFinite(rate)) return '';
  return `${Math.round(rate * 100)}%`;
}

function getPriceMeta(val) {
  const raw = String(val ?? '').trim();
  if (!raw) return { raw: '', amount: NaN, symbol: '' };
  const symbolMatch = raw.match(/[€$£¥]/);
  return {
    raw,
    amount: parsePrice(raw),
    symbol: symbolMatch ? symbolMatch[0] : '',
  };
}

function formatPrice(val) {
  const meta = getPriceMeta(val);
  if (!meta.raw) return '-';
  if (!Number.isFinite(meta.amount) || meta.amount <= 0) return meta.raw;
  const formattedAmount = new Intl.NumberFormat(getLocaleForLang(currentLang), {
    maximumFractionDigits: 0,
  }).format(meta.amount);
  return meta.symbol ? `${meta.symbol}${formattedAmount}` : formattedAmount;
}

function getConsumptionInfo(vehicle) {
  const info = vehicle?.consumption;
  if (!info || typeof info.value !== 'number') return null;
  return info;
}

function getConsumptionType(info) {
  const unit = String(info?.unit || '').toLowerCase();
  return unit.includes('kwh') ? 'electric' : 'fuel';
}

const DEFAULT_PRICE_PER_LITER = 1.7;
const DEFAULT_PRICE_PER_KWH = 0.25;

function calculateCost(vehicle) {
  const info = getConsumptionInfo(vehicle);
  if (!info) return null;
  const rate = getConsumptionType(info) === 'electric'
    ? getStoredNumber('pricePerKwh', DEFAULT_PRICE_PER_KWH, 100)
    : getStoredNumber('pricePerLiter', DEFAULT_PRICE_PER_LITER, 100);
  const value = Number(info.value);
  if (!Number.isFinite(value) || value <= 0) return null;
  if (!Number.isFinite(rate) || rate <= 0) return null;
  return value * rate;
}

function formatCurrency(value) {
  if (!Number.isFinite(value)) return '-';
  return `\u20AC${value.toFixed(2)}`;
}

function formatCostValue(value) {
  if (value === null || value === undefined || value === '') return '-';
  if (typeof value === 'number' && Number.isFinite(value)) return formatCurrency(value);
  return String(value);
}

function getStoredNumber(key, fallback, maxValue = Infinity) {
  const raw = localStorage.getItem(key);
  if (raw === null || raw === '') return fallback;
  const normalized = String(raw).replace(',', '.');
  const num = Number(normalized);
  return Number.isFinite(num) && num > 0 && num <= maxValue ? num : fallback;
}

function setStoredNumber(key, value) {
  if (!Number.isFinite(value)) return;
  localStorage.setItem(key, String(value));
}

const FUEL_DISTANCE_KEY = 'fuelCalcDistance';
const FUEL_UNIT_KEY = 'fuelCalcUnit';
const FUEL_CONSUMPTION_L_KEY = 'fuelCalcConsumptionL';
const FUEL_CONSUMPTION_KWH_KEY = 'fuelCalcConsumptionKwh';

function parseNumberInput(value) {
  const normalized = String(value ?? '').replace(',', '.').trim();
  const num = Number(normalized);
  return Number.isFinite(num) ? num : NaN;
}

function getFuelUnit() {
  return fuelCalcUnit && fuelCalcUnit.value === 'electric' ? 'electric' : 'fuel';
}

function getConsumptionKey(unit) {
  return unit === 'electric' ? FUEL_CONSUMPTION_KWH_KEY : FUEL_CONSUMPTION_L_KEY;
}

function getPriceKey(unit) {
  return unit === 'electric' ? 'pricePerKwh' : 'pricePerLiter';
}

function getDefaultPrice(unit) {
  return unit === 'electric' ? DEFAULT_PRICE_PER_KWH : DEFAULT_PRICE_PER_LITER;
}

function getConsumptionUnit(unit) {
  return unit === 'electric' ? 'kWh/100km' : 'L/100km';
}

function loadFuelInputsForUnit(unit) {
  if (fuelCalcPrice) {
    fuelCalcPrice.value = getStoredNumber(getPriceKey(unit), getDefaultPrice(unit), 100);
  }
  if (fuelCalcConsumption) {
    const savedConsumption = localStorage.getItem(getConsumptionKey(unit));
    fuelCalcConsumption.value = savedConsumption !== null ? savedConsumption : '';
  }
}

function syncFuelCalculatorToSelection(force = false) {
  if (!fuelCalcUnit || !fuelCalcConsumption || selected.length === 0) return;
  const preferredVehicle = selected.find(v => getConsumptionInfo(v));
  if (!preferredVehicle) return;
  const info = getConsumptionInfo(preferredVehicle);
  if (!info) return;
  const preferredUnit = getConsumptionType(info);
  const currentUnit = getFuelUnit();
  const currentConsumption = parseNumberInput(fuelCalcConsumption.value);
  if (force || currentUnit !== preferredUnit) {
    fuelCalcUnit.value = preferredUnit;
    localStorage.setItem(FUEL_UNIT_KEY, preferredUnit);
    loadFuelInputsForUnit(preferredUnit);
  }
  if (force || currentUnit !== preferredUnit || !Number.isFinite(currentConsumption) || currentConsumption <= 0) {
    fuelCalcConsumption.value = String(info.value);
  }
  updateFuelCalcLabels();
  updateFuelCalculator();
}

function updateFuelCalcLabels() {
  const pack = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const unit = getFuelUnit();
  const fuelUnitLabel = document.getElementById('fuelCalcUnitLabel');
  const fuelUnitSelect = document.getElementById('fuelCalcUnit');
  const fuelPriceLabel = document.getElementById('fuelCalcPriceLabel');
  const fuelConsumptionLabel = document.getElementById('fuelCalcConsumptionLabel');

  if (fuelUnitLabel) fuelUnitLabel.textContent = pack.unitLabel || 'Unit';
  if (fuelUnitSelect) {
    const fuelOpt = fuelUnitSelect.querySelector('option[value="fuel"]');
    const elecOpt = fuelUnitSelect.querySelector('option[value="electric"]');
    if (fuelOpt) fuelOpt.textContent = pack.unitFuel || 'Fuel (L/100km)';
    if (elecOpt) elecOpt.textContent = pack.unitElectric || 'Electric (kWh/100km)';
  }
  if (fuelPriceLabel) {
    const currency = getCurrencyForLang(currentLang);
    const baseLabel = unit === 'electric' ? pack.pricePerKwh : pack.pricePerLiter;
    fuelPriceLabel.textContent = `${baseLabel} (${currency})`;
  }
  if (fuelConsumptionLabel) {
    const consumptionLabel = pack.consumptionLabel || 'Consumption';
    fuelConsumptionLabel.textContent = `${consumptionLabel} (${getConsumptionUnit(unit)})`;
  }
}

function isFuelPremiumLocked() {
  return !hasPremiumAccess;
}

function updateFuelPremiumUi() {
  const pack = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const locked = isFuelPremiumLocked();
  if (fuelCard) fuelCard.classList.toggle('is-locked', locked);
  if (fuelPremiumLock) fuelPremiumLock.classList.toggle('hidden', !locked);
  if (fuelPremiumBadge) fuelPremiumBadge.textContent = pack.premiumBadge || 'Premium';
  if (fuelPremiumLockText) {
    fuelPremiumLockText.textContent = pack.premiumCostLocked || 'Cost of Ownership is a premium feature.';
  }
  if (fuelPremiumUnlockBtn) {
    fuelPremiumUnlockBtn.textContent = locked
      ? (sessionUserId ? (pack.premiumUnlock || 'Upgrade to Unlock') : (pack.login || 'Log In'))
      : (pack.premiumBadge || 'Premium');
  }
  [fuelCalcDistance, fuelCalcPrice, fuelCalcUnit, fuelCalcConsumption].forEach((input) => {
    if (!input) return;
    input.disabled = locked;
  });
}

function updateFuelCalculator() {
  if (!fuelCalcSection || !fuelCalcResult) return;
  if (isFuelPremiumLocked()) {
    fuelCalcResult.textContent = '-';
    return;
  }
  const unit = getFuelUnit();
  const priceKey = getPriceKey(unit);
  const consumptionKey = getConsumptionKey(unit);
  const distance = parseNumberInput(fuelCalcDistance?.value);
  const price = parseNumberInput(fuelCalcPrice?.value);
  const consumption = parseNumberInput(fuelCalcConsumption?.value);

  if (Number.isFinite(price) && price > 0) {
    setStoredNumber(priceKey, price);
  }
  if (Number.isFinite(distance) && distance >= 0) {
    localStorage.setItem(FUEL_DISTANCE_KEY, String(distance));
  }
  if (Number.isFinite(consumption) && consumption > 0) {
    localStorage.setItem(consumptionKey, String(consumption));
  }

  if (!Number.isFinite(distance) || distance < 0) {
    fuelCalcResult.textContent = '-';
    return;
  }
  if (!Number.isFinite(price) || price <= 0 || !Number.isFinite(consumption) || consumption <= 0) {
    fuelCalcResult.textContent = '-';
    return;
  }

  const total = (distance / 100) * consumption * price;
  fuelCalcResult.textContent = formatCurrency(total);
}

function setFuelCalculatorVisible(visible) {
  if (!fuelCalcSection) return;
  fuelCalcSection.classList.toggle('hidden', !visible);
}

function initFuelCalculator() {
  if (!fuelCalcSection) return;
  const savedDistance = localStorage.getItem(FUEL_DISTANCE_KEY);
  if (fuelCalcDistance && savedDistance !== null) fuelCalcDistance.value = savedDistance;
  const savedUnit = localStorage.getItem(FUEL_UNIT_KEY);
  if (fuelCalcUnit && (savedUnit === 'fuel' || savedUnit === 'electric')) {
    fuelCalcUnit.value = savedUnit;
  }
  const unit = getFuelUnit();
  loadFuelInputsForUnit(unit);
  updateFuelCalcLabels();
  updateFuelPremiumUi();

  [fuelCalcDistance, fuelCalcPrice, fuelCalcConsumption].forEach((input) => {
    if (!input) return;
    input.addEventListener('input', updateFuelCalculator);
    input.addEventListener('change', updateFuelCalculator);
  });
  if (fuelCalcUnit) {
    fuelCalcUnit.addEventListener('change', () => {
      const nextUnit = getFuelUnit();
      localStorage.setItem(FUEL_UNIT_KEY, nextUnit);
      loadFuelInputsForUnit(nextUnit);
      updateFuelCalcLabels();
      updateFuelCalculator();
    });
  }

  updateFuelCalculator();
}

function getMetaContent(name) {
  const meta = document.querySelector(`meta[name="${name}"]`);
  return meta ? String(meta.getAttribute('content') || '').trim() : '';
}

const paddleClientToken = getMetaContent('paddle-client-token');
const paddleEnv = (getMetaContent('paddle-env') || 'sandbox').toLowerCase();
let paddleInitialized = false;
let paddleEventsBound = false;

function getPaddleLocale() {
  const code = String(currentLang || 'en').trim();
  const normalized = code.toLowerCase();
  const allowed = new Set([
    'en', 'tr', 'de', 'fr', 'es', 'it', 'nl', 'sv', 'no', 'da', 'pl', 'pt', 'pt-br',
    'ru', 'ja', 'ko', 'zh-hans', 'zh-hant', 'ar'
  ]);
  if (allowed.has(normalized)) {
    return normalized === 'pt-br' ? 'pt-BR' : normalized;
  }
  return 'en';
}

function initPaddleCheckout() {
  if (paddleInitialized) return true;
  if (!paddleClientToken) return false;
  if (!window.Paddle || typeof window.Paddle.Initialize !== 'function') return false;
  try {
    if (window.Paddle.Environment && typeof window.Paddle.Environment.set === 'function') {
      window.Paddle.Environment.set(paddleEnv === 'production' ? 'production' : 'sandbox');
    }
    window.Paddle.Initialize({ token: paddleClientToken });
    bindPaddleEvents();
    paddleInitialized = true;
    return true;
  } catch (err) {
    console.error('Paddle init failed', err);
    return false;
  }
}

function extractTransactionIdFromEvent(data) {
  if (!data || typeof data !== 'object') return '';
  return (
    data.transactionId
    || data.transaction_id
    || (data.transaction && (data.transaction.id || data.transaction.transaction_id))
    || ''
  );
}

function bindPaddleEvents() {
  if (paddleEventsBound) return;
  if (!window.Paddle || !window.Paddle.Checkout || typeof window.Paddle.Checkout.on !== 'function') return;
  window.Paddle.Checkout.on('complete', async (data) => {
    const txnId = extractTransactionIdFromEvent(data) || getPendingPaddleTxn();
    if (txnId) {
      setPendingPaddleTxn(String(txnId));
      const confirmed = await confirmPaddleTransaction(String(txnId));
      if (confirmed) {
        setPendingPaddleTxn('');
        window.location.reload();
        return;
      }
      startPendingConfirmPolling();
      return;
    }
    window.location.reload();
  });
  paddleEventsBound = true;
}

function openPaddleCheckout(transactionId) {
  if (!transactionId) return false;
  if (!initPaddleCheckout()) return false;
  if (!window.Paddle || !window.Paddle.Checkout || typeof window.Paddle.Checkout.open !== 'function') {
    return false;
  }
  try {
    window.Paddle.Checkout.open({
      transactionId,
      settings: {
        locale: getPaddleLocale(),
      },
    });
    return true;
  } catch (err) {
    console.error('Paddle checkout failed', err);
    return false;
  }
}

function extractTransactionId(urlString) {
  if (!urlString) return '';
  try {
    const url = new URL(urlString, window.location.origin);
    return url.searchParams.get('_ptxn') || url.searchParams.get('transaction_id') || '';
  } catch (err) {
    return '';
  }
}

const PENDING_PADDLE_TXN_KEY = 'pendingPaddleTxn';
let pendingPaddleTxn = '';
let pendingConfirmTimer = null;
let pendingConfirmAttempts = 0;
const PENDING_CONFIRM_INTERVAL_MS = 5000;
const PENDING_CONFIRM_MAX_ATTEMPTS = 24;

async function confirmPaddleTransaction(transactionId) {
  if (!transactionId) return false;
  if (!sessionUserId) return false;
  try {
    const res = await fetch('/api/billing/confirm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transaction_id: transactionId }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data && data.ok) {
      unlockPremiumUi();
      return true;
    }
  } catch (err) {
    console.warn('Confirm transaction failed', err);
  }
  return false;
}

function stopPendingConfirmPolling() {
  if (pendingConfirmTimer) {
    clearInterval(pendingConfirmTimer);
    pendingConfirmTimer = null;
  }
  pendingConfirmAttempts = 0;
}

function startPendingConfirmPolling() {
  if (pendingConfirmTimer) return;
  pendingConfirmAttempts = 0;
  pendingConfirmTimer = setInterval(async () => {
    const txn = getPendingPaddleTxn();
    if (!txn) {
      stopPendingConfirmPolling();
      return;
    }
    const confirmed = await confirmPaddleTransaction(txn);
    if (confirmed) {
      setPendingPaddleTxn('');
      stopPendingConfirmPolling();
      window.location.reload();
      return;
    }
    pendingConfirmAttempts += 1;
    if (pendingConfirmAttempts >= PENDING_CONFIRM_MAX_ATTEMPTS) {
      stopPendingConfirmPolling();
    }
  }, PENDING_CONFIRM_INTERVAL_MS);
}

function setPendingPaddleTxn(txnId) {
  pendingPaddleTxn = txnId || '';
  if (pendingPaddleTxn) {
    sessionStorage.setItem(PENDING_PADDLE_TXN_KEY, pendingPaddleTxn);
  } else {
    sessionStorage.removeItem(PENDING_PADDLE_TXN_KEY);
  }
}

function getPendingPaddleTxn() {
  if (pendingPaddleTxn) return pendingPaddleTxn;
  const stored = sessionStorage.getItem(PENDING_PADDLE_TXN_KEY);
  if (stored) {
    pendingPaddleTxn = stored;
  }
  return pendingPaddleTxn;
}

async function handlePendingPaddleCheckout() {
  const urlTxn = new URLSearchParams(window.location.search).get('_ptxn');
  if (urlTxn) {
    setPendingPaddleTxn(urlTxn);
    const cleanUrl = window.location.pathname + window.location.hash;
    window.history.replaceState({}, document.title, cleanUrl);
  }
  const pending = getPendingPaddleTxn();
  if (!pending) return;
  const confirmed = await confirmPaddleTransaction(pending);
  if (confirmed) {
    setPendingPaddleTxn('');
    window.location.reload();
    return;
  }
  startPendingConfirmPolling();
  if (fuelPremiumUnlockBtn) {
    fuelPremiumUnlockBtn.disabled = false;
    fuelPremiumUnlockBtn.textContent = t('premiumCheckoutResume');
  }
}

handlePendingPaddleCheckout();

async function startFuelPremiumCheckout() {
  if (!isFuelPremiumLocked()) return;
  if (!sessionUserId) {
    setAuthMode('login');
    openLoginModal();
    return;
  }
  if (!fuelPremiumUnlockBtn) return;
  const loadingLabel = t('premiumCheckoutLoading');
  const originalLabel = fuelPremiumUnlockBtn.textContent;
  fuelPremiumUnlockBtn.disabled = true;
  fuelPremiumUnlockBtn.textContent = loadingLabel;
  try {
    const pending = getPendingPaddleTxn();
    if (pending) {
      const confirmed = await confirmPaddleTransaction(pending);
      if (confirmed) {
        setPendingPaddleTxn('');
        window.location.reload();
        return;
      }
      startPendingConfirmPolling();
      if (openPaddleCheckout(pending)) {
        return;
      }
      throw new Error(t('premiumCheckoutError'));
    }
    const res = await fetch('/api/billing/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feature: 'cost_of_ownership' }),
    });
    let data = {};
    try {
      data = await res.json();
    } catch (err) {
      data = {};
    }
    if (!res.ok || !data.ok || !data.checkout_url) {
      const backendDetail = (() => {
        if (!data || typeof data !== 'object') return '';
        if (data.message) return String(data.message);
        const details = data.details;
        if (details && typeof details === 'object') {
          if (details.error && typeof details.error === 'object') {
            return String(details.error.detail || details.error.message || '').trim();
          }
          if (Array.isArray(details.errors) && details.errors.length) {
            const first = details.errors[0];
            if (first && typeof first === 'object') {
              return String(first.detail || first.message || '').trim();
            }
          }
        }
        return '';
      })();
      throw new Error(backendDetail || t('premiumCheckoutError'));
    }
    const checkoutUrl = String(data.checkout_url || '');
    const transactionId = extractTransactionId(checkoutUrl) || data.transaction_id;
    if (transactionId) {
      setPendingPaddleTxn(String(transactionId));
      startPendingConfirmPolling();
    }
    if (!openPaddleCheckout(transactionId)) {
      if (transactionId) {
        setPendingPaddleTxn(transactionId);
      }
      window.location.href = checkoutUrl;
    }
  } catch (err) {
    alert(err?.message || t('premiumCheckoutError'));
    fuelPremiumUnlockBtn.disabled = false;
    fuelPremiumUnlockBtn.textContent = originalLabel;
  }
}

if (fuelPremiumUnlockBtn) {
  fuelPremiumUnlockBtn.addEventListener('click', startFuelPremiumCheckout);
}


function sortVehicles(list) {
  if (!activeSort) return list;
  const sorted = [...list];
  sorted.sort((a, b) => {
    if (activeSort === 'topSpeed') {
      return Number(b.topSpeed || 0) - Number(a.topSpeed || 0);
    }
    if (activeSort === 'nameAZ') {
      return 0;
    }
    if (activeSort === 'acc') {
      return Number(a.acc || 0) - Number(b.acc || 0);
    }
    if (activeSort === 'price') {
      return parsePrice(b.price) - parsePrice(a.price);
    }
    return 0;
  });
  return sorted;
}

function setupLazyThumbs(container) {
  if (!container) return;
  const imgs = container.querySelectorAll('img[data-src]');
  if (!imgs.length) return;
  if (listLazyObserver) listLazyObserver.disconnect();
  if (!('IntersectionObserver' in window)) {
    imgs.forEach(loadDeferredImage);
    return;
  }
  listLazyObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const img = entry.target;
      loadDeferredImage(img);
      observer.unobserve(img);
    });
  }, { root: container, rootMargin: '500px 0px', threshold: 0.01 });
  imgs.forEach(img => listLazyObserver.observe(img));
}

// render sidebar list
function renderList(filter = '') {
  listEl.innerHTML = '';
  const q = filter.trim().toLowerCase();
  const brandFilter = activeBrand && activeBrand !== 'all' ? activeBrand.toLowerCase() : '';
  const filtered = currentInventory().filter(v => {
    const haystack = (v.name + ' ' + v.engine).toLowerCase();
    if (q && !haystack.includes(q)) return false;
    if (brandFilter) {
      const brand = getBrandLabel(v.name).toLowerCase();
      if (brand !== brandFilter) return false;
    }
    return true;
  });
  const ordered = sortVehicles(filtered);
  const useBrandGrouping = (!activeSort || activeSort === 'nameAZ') && !brandFilter;
  const eagerImageCount = getInitialListImageCount();
  let lastBrand = null;

  ordered.forEach((v, index) => {
    const brand = getBrandLabel(v.name);
    if (useBrandGrouping && brand !== lastBrand) {
      listEl.appendChild(createBrandDivider(brand));
    }
    const item = document.createElement('div');
    item.className = 'item';
    const thumb = safeImg(resolveMainImage(v), v.name);
    const key = makeKey(activeCatalog, v.id);
    const favActive = favoritesEnabled && isFavorite(key);
    const favLabel = favActive ? t('removeFavorite') : t('addFavorite');
    const actionsHtml = favoritesEnabled
      ? `
        <div class="item-actions">
          <button class="add-btn" data-id="${key}" aria-label="${t('add')} ${v.name}">${t('add')}</button>
          <button class="fav-btn ${favActive ? 'active' : ''}" data-id="${key}" aria-label="${favLabel}" title="${favLabel}">${favActive ? HEART_FILLED : HEART_EMPTY}</button>
        </div>
      `
      : `
        <button class="add-btn" data-id="${key}" aria-label="${t('add')} ${v.name}">${t('add')}</button>
      `;
    const shouldEagerLoad = index < eagerImageCount;
    const imgAttrs = shouldEagerLoad
      ? `src="${thumb}" loading="eager" fetchpriority="${index < 4 ? 'high' : 'auto'}"`
      : `data-src="${thumb}" src="${TINY_IMG}" loading="lazy" fetchpriority="low"`;
    item.innerHTML = `
      <img class="thumb list-thumb" ${imgAttrs} alt="${v.name}" decoding="async" width="88" height="56" />
      <div class="info">
        <h3>${v.name}</h3>
        <p>${v.engine} · ${v.power} CV · ${v.topSpeed} km/h</p>
      </div>
      ${actionsHtml}
    `;
    listEl.appendChild(item);
    if (useBrandGrouping) lastBrand = brand;
  });
  attachAddButtons();
  attachListFavoriteButtons();
  setupLazyThumbs(listEl);
}

// attach add listeners
function attachAddButtons() {
  listEl.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parsed = parseKey(btn.dataset.id);
      const source = parsed.catalog === 'motorcycles' ? MOTORCYCLES : VEHICLES;
      const veh = source.find(x => String(x.id) === parsed.id);
      if (!veh) return;
      const key = makeKey(parsed.catalog, parsed.id);
      if (selected.find(s => (s._key || makeKey(s.catalog || 'cars', s.id)) === key)) return;
      if (selected.length >= compareLimit) {
        alert(hasPremiumAccess ? t('maxComparePremium') : t('maxCompare'));
        return;
      }
      selected.push({ ...veh, _key: key, catalog: parsed.catalog });
      if (selected.length === 1) {
        setMobileSidebarCollapsed(true);
      }
      renderSelected();
    });
  });
}

// render selected area
function renderSelected() {
  compareArea.innerHTML = '';
  if (selected.length === 0) {
    setMobileSidebarCollapsed(false);
    const emptyNoteText = t('emptyNote');
    compareArea.innerHTML = `
      <div class="empty-block">
        <p class="empty">${t('empty')}</p>
        <p class="empty-note">${emptyNoteText === 'emptyNote' ? 'Prices reflect estimated market values and may vary by region.' : emptyNoteText}</p>
      </div>
    `;
    compTable.innerHTML = '';
    if (tableArea) tableArea.classList.add('hidden');
    renderCompareDecisionSection();
    renderComparisonRaceLinks();
    setFuelCalculatorVisible(false);
    updateMobileVehicleToggle();
    return;
  }

  selected.forEach(v => {
    const card = document.createElement('div');
    card.className = 'compare-card';
    const thumb = safeImg(resolveMainImage(v), v.name);
    const rearSrc = resolveRearImage(v);
    const rearThumb = rearSrc ? safeImg(rearSrc, `${v.name} rear`) : null;
    const gallery = [thumb, rearThumb].filter(Boolean);
    const startSrc = gallery[0] || thumb;
    const catalog = v.catalog || 'cars';
    const key = v._key || makeKey(catalog, v.id);
    const detailLink = catalog === 'cars'
      ? `<a class="detail-btn" href="${buildCarDetailUrl(v)}" aria-label="${t('details')} ${v.name}">${t('details')}</a>`
      : '';
    const resale = buildResalePrediction(v);
    const resaleAllowed = hasPremiumAccess;
    const resalePanel = (resale && resaleAllowed) ? `
      <div class="resale-panel hidden" data-id="${key}">
        <div class="resale-title">${t('resaleTitle')}</div>
        <div class="resale-meta">${resale.kind === 'appreciation' ? t('resaleAppreciation') : t('resaleDepreciation')}: ${formatRate(resale.rate)} · ${resale.categoryLabel}</div>
        <div class="resale-values">
          <span>${t('resaleYear5')}: ${formatCurrency(resale.values[0])}</span>
          <span>${t('resaleYear10')}: ${formatCurrency(resale.values[1])}</span>
          <span>${t('resaleYear15')}: ${formatCurrency(resale.values[2])}</span>
        </div>
      </div>
    ` : '';
    const resaleButton = resale
      ? (
        resaleAllowed
          ? `<button class="resale-btn" type="button" data-id="${key}">${t('resaleButton')}</button>`
          : `<button class="resale-btn locked" type="button" data-locked="1">${t('premiumUnlock')}</button>`
      )
      : '';
    card.innerHTML = `
      <div class="thumb-row single">
        <div class="thumb-frame" style="--thumb-bg:url('${startSrc}')">
          <span class="thumb-badge">${v.id}</span>
          <img class="thumb thumb-img" data-src="${startSrc}" data-gallery="${gallery.join('|')}" data-index="0" src="${startSrc}" alt="${v.name}" loading="eager" decoding="async" fetchpriority="high" />
        </div>
      </div>
      <div class="meta">
        <h4>${v.name}</h4>
        <div class="spec-line">${v.engine} - ${v.power} CV - ${v.topSpeed} km/h</div>
        <div class="price-wrapper">
          <span class="price-label">${t('priceLabel')}</span>
          <span class="price-value">${formatPrice(v.price)}</span>
          ${resaleButton}
        </div>
        ${resalePanel}
        <div class="stat-line"><strong>${t('zeroToHundred')}</strong> ${v.acc}s</div>
        <div class="card-actions">
        <button class="remove-btn" data-id="${key}" aria-label="${t('remove')} ${v.name}">${t('remove')}</button>
          ${detailLink}
        </div>
      </div>
    `;
    const mainThumb = card.querySelector('.thumb-img');
    if (mainThumb) {
      const applyVisual = () => {
        applyFitMode(mainThumb);
        applyCardAccent(card, mainThumb);
      };
      mainThumb.addEventListener('load', applyVisual);
      if (mainThumb.complete) applyVisual();
      const galleryImgs = gallery.length ? gallery : [thumb].filter(Boolean);
      mainThumb.addEventListener('click', () => {
        if (galleryImgs.length > 1) {
          const nextIdx = (Number(mainThumb.dataset.index || 0) + 1) % galleryImgs.length;
          const nextSrc = galleryImgs[nextIdx];
          mainThumb.dataset.index = nextIdx;
          mainThumb.dataset.src = nextSrc;
          mainThumb.src = nextSrc;
          return;
        }
        if (mainThumb.dataset.src) {
          openLightbox(mainThumb.dataset.src);
        }
      });
    }
    compareArea.appendChild(card);
  });

  renderCompareDecisionSection();
  renderComparisonRaceLinks();
  syncFuelCalculatorToSelection();
  updateMobileVehicleToggle();

  // attach remove handlers
  compareArea.querySelectorAll('.remove-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      selected = selected.filter(s => (s._key || makeKey(s.catalog || 'cars', s.id)) !== id);
      renderSelected();
    });
  });
  compareArea.querySelectorAll('.resale-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (btn.dataset.locked === '1') {
        startFuelPremiumCheckout();
        return;
      }
      const id = btn.dataset.id;
      if (!id) return;
      const panel = compareArea.querySelector(`.resale-panel[data-id="${id}"]`);
      if (!panel) return;
      panel.classList.toggle('hidden');
    });
  });
}

function buildYoutubeRaceSearchQuery(leftVehicle, rightVehicle) {
  const leftName = String(leftVehicle?.name || leftVehicle?.id || 'Vehicle A').trim();
  const rightName = String(rightVehicle?.name || rightVehicle?.id || 'Vehicle B').trim();
  return `${leftName} vs ${rightName} drag race`;
}

function buildYoutubeRaceSearchUrl(leftVehicle, rightVehicle) {
  return `https://www.youtube.com/results?search_query=${encodeURIComponent(buildYoutubeRaceSearchQuery(leftVehicle, rightVehicle))}`;
}

function getComparisonRaceLinks(vehicles) {
  const links = [];
  const seen = new Set();
  for (let i = 0; i < vehicles.length; i += 1) {
    for (let j = i + 1; j < vehicles.length; j += 1) {
      const left = vehicles[i];
      const right = vehicles[j];
      const leftKey = left?._key || makeKey(left?.catalog || 'cars', left?.id);
      const rightKey = right?._key || makeKey(right?.catalog || 'cars', right?.id);
      const pairKey = [leftKey, rightKey].sort().join('::');
      if (seen.has(pairKey)) continue;
      seen.add(pairKey);
      links.push({
        key: pairKey,
        title: `${left.name} vs ${right.name}`,
        url: buildYoutubeRaceSearchUrl(left, right),
      });
    }
  }
  return links;
}

function extractModelYear(vehicle) {
  const match = String(vehicle?.name || '').match(/\b(19|20)\d{2}\b/);
  return match ? Number(match[0]) : null;
}

function compareNumericValues(leftValue, rightValue, higherIsBetter = true) {
  if (!Number.isFinite(Number(leftValue)) || !Number.isFinite(Number(rightValue))) return null;
  const left = Number(leftValue);
  const right = Number(rightValue);
  if (left === right) return null;
  if (higherIsBetter) return left > right ? 'left' : 'right';
  return left < right ? 'left' : 'right';
}

function joinDecisionLabels(items) {
  if (!items || !items.length) return '';
  if (items.length === 1) return items[0];
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(', ')}, and ${items[items.length - 1]}`;
}

function pushUnique(list, value) {
  if (value && !list.includes(value)) list.push(value);
}

function buildCompareDecisionData(leftVehicle, rightVehicle) {
  if (!leftVehicle || !rightVehicle) return null;

  const leftName = String(leftVehicle.name || leftVehicle.id || 'Vehicle A').trim();
  const rightName = String(rightVehicle.name || rightVehicle.id || 'Vehicle B').trim();
  const leftPrice = getPriceMeta(leftVehicle.price).amount;
  const rightPrice = getPriceMeta(rightVehicle.price).amount;
  const leftConsumption = getConsumptionInfo(leftVehicle);
  const rightConsumption = getConsumptionInfo(rightVehicle);
  const leftYear = extractModelYear(leftVehicle);
  const rightYear = extractModelYear(rightVehicle);

  const powerWinner = compareNumericValues(leftVehicle.power, rightVehicle.power, true);
  const accWinner = compareNumericValues(leftVehicle.acc, rightVehicle.acc, false);
  const topSpeedWinner = compareNumericValues(leftVehicle.topSpeed, rightVehicle.topSpeed, true);
  const priceWinner = compareNumericValues(leftPrice, rightPrice, false);
  const yearWinner = compareNumericValues(leftYear, rightYear, true);
  const consumptionWinner = (
    leftConsumption &&
    rightConsumption &&
    String(leftConsumption.unit || '').toLowerCase() === String(rightConsumption.unit || '').toLowerCase()
  ) ? compareNumericValues(leftConsumption.value, rightConsumption.value, false) : null;

  const performanceScores = { left: 0, right: 0 };
  const performanceLabels = { left: [], right: [] };
  [
    [powerWinner, 'power'],
    [accWinner, '0-100 km/h'],
    [topSpeedWinner, 'top speed'],
  ].forEach(([winner, label]) => {
    if (!winner) return;
    performanceScores[winner] += 1;
    performanceLabels[winner].push(label);
  });

  let performanceWinner = null;
  if (performanceScores.left !== performanceScores.right) {
    performanceWinner = performanceScores.left > performanceScores.right ? 'left' : 'right';
  } else {
    performanceWinner = accWinner || powerWinner || topSpeedWinner;
  }

  const valueScores = { left: 0, right: 0 };
  const valueLabels = { left: [], right: [] };
  [
    [priceWinner, 'price'],
    [consumptionWinner, 'efficiency'],
    [yearWinner, 'model year'],
  ].forEach(([winner, label]) => {
    if (!winner) return;
    valueScores[winner] += 1;
    valueLabels[winner].push(label);
  });

  let valueWinner = null;
  if (valueScores.left !== valueScores.right) {
    valueWinner = valueScores.left > valueScores.right ? 'left' : 'right';
  } else {
    valueWinner = priceWinner || consumptionWinner || yearWinner;
  }

  const speedWinner = topSpeedWinner || accWinner || performanceWinner;
  const overallScores = { left: 0, right: 0 };
  [powerWinner, accWinner, topSpeedWinner, priceWinner, consumptionWinner, yearWinner, performanceWinner, valueWinner, speedWinner].forEach((winner) => {
    if (winner) overallScores[winner] += 1;
  });

  let overallWinner = null;
  if (overallScores.left !== overallScores.right) {
    overallWinner = overallScores.left > overallScores.right ? 'left' : 'right';
  } else {
    overallWinner = performanceWinner || valueWinner || speedWinner;
  }

  const winnerName = {
    left: leftName,
    right: rightName,
    null: 'Too close to call',
  };

  const verdicts = [
    {
      label: 'Performance winner',
      winner: winnerName[performanceWinner ?? 'null'],
      reason: performanceWinner
        ? `Leads on ${joinDecisionLabels(performanceLabels[performanceWinner])}.`
        : 'No clear edge on the recorded performance data.',
    },
    {
      label: 'Speed winner',
      winner: winnerName[speedWinner ?? 'null'],
      reason: speedWinner
        ? (topSpeedWinner === speedWinner ? 'Higher top speed on paper.' : 'Quicker acceleration on paper.')
        : 'No clear speed advantage on the recorded data.',
    },
    {
      label: 'Value winner',
      winner: winnerName[valueWinner ?? 'null'],
      reason: valueWinner
        ? `Stronger on ${joinDecisionLabels(valueLabels[valueWinner])}.`
        : 'No clear value edge on price, efficiency, or model year.',
    },
    {
      label: 'Overall winner',
      winner: winnerName[overallWinner ?? 'null'],
      reason: overallWinner
        ? 'Wins more of the recorded comparison categories overall.'
        : 'The available data is too evenly matched to separate them.',
    },
  ];

  const leftPros = [];
  const leftCons = [];
  const rightPros = [];
  const rightCons = [];

  if (powerWinner === 'left') {
    pushUnique(leftPros, 'More power');
    pushUnique(rightCons, 'Less power');
  } else if (powerWinner === 'right') {
    pushUnique(rightPros, 'More power');
    pushUnique(leftCons, 'Less power');
  }

  if (accWinner === 'left') {
    pushUnique(leftPros, 'Quicker 0-100 km/h');
    pushUnique(rightCons, 'Slower off the line');
  } else if (accWinner === 'right') {
    pushUnique(rightPros, 'Quicker 0-100 km/h');
    pushUnique(leftCons, 'Slower off the line');
  }

  if (topSpeedWinner === 'left') {
    pushUnique(leftPros, 'Higher top speed');
    pushUnique(rightCons, 'Lower top speed');
  } else if (topSpeedWinner === 'right') {
    pushUnique(rightPros, 'Higher top speed');
    pushUnique(leftCons, 'Lower top speed');
  }

  if (priceWinner === 'left') {
    pushUnique(leftPros, 'Lower price');
    pushUnique(rightCons, 'Higher price');
  } else if (priceWinner === 'right') {
    pushUnique(rightPros, 'Lower price');
    pushUnique(leftCons, 'Higher price');
  }

  if (consumptionWinner === 'left') {
    pushUnique(leftPros, 'Better efficiency');
    pushUnique(rightCons, 'Higher fuel consumption');
  } else if (consumptionWinner === 'right') {
    pushUnique(rightPros, 'Better efficiency');
    pushUnique(leftCons, 'Higher fuel consumption');
  }

  if (yearWinner === 'left') {
    pushUnique(leftPros, 'Newer model year');
    pushUnique(rightCons, 'Older model year');
  } else if (yearWinner === 'right') {
    pushUnique(rightPros, 'Newer model year');
    pushUnique(leftCons, 'Older model year');
  }

  if (!leftPros.length) pushUnique(leftPros, 'Competitive overall spec balance');
  if (!rightPros.length) pushUnique(rightPros, 'Competitive overall spec balance');
  if (!leftCons.length) pushUnique(leftCons, 'Few clear weaknesses in the recorded specs');
  if (!rightCons.length) pushUnique(rightCons, 'Few clear weaknesses in the recorded specs');

  return {
    verdicts,
    tradeoffs: [
      { title: leftName, pros: leftPros.slice(0, 3), cons: leftCons.slice(0, 3) },
      { title: rightName, pros: rightPros.slice(0, 3), cons: rightCons.slice(0, 3) },
    ],
  };
}

function getDecisionVehicleKey(vehicle) {
  return vehicle?._key || makeKey(vehicle?.catalog || 'cars', vehicle?.id);
}

function getDecisionVehicleName(vehicle) {
  return String(vehicle?.name || vehicle?.id || 'Unknown vehicle').trim();
}

function formatDecisionWinnerNames(vehicles) {
  if (!vehicles || !vehicles.length) return 'Too close to call';
  return joinDecisionLabels(vehicles.map(getDecisionVehicleName));
}

function getNumericDecisionMeta(vehicles, getValue, higherIsBetter = true) {
  const values = vehicles
    .map((vehicle) => ({ vehicle, value: Number(getValue(vehicle)) }))
    .filter((entry) => Number.isFinite(entry.value));

  if (values.length < 2) {
    return { leaders: [], comparable: false };
  }

  const bestValue = higherIsBetter
    ? Math.max(...values.map((entry) => entry.value))
    : Math.min(...values.map((entry) => entry.value));

  return {
    leaders: values
      .filter((entry) => entry.value === bestValue)
      .map((entry) => entry.vehicle),
    comparable: true,
  };
}

function getConsumptionDecisionMeta(vehicles) {
  const values = vehicles
    .map((vehicle) => ({ vehicle, info: getConsumptionInfo(vehicle) }))
    .filter((entry) => entry.info && Number.isFinite(Number(entry.info.value)));

  if (values.length < 2) {
    return { leaders: [], comparable: false };
  }

  const units = new Set(values.map((entry) => String(entry.info.unit || '').toLowerCase()));
  if (units.size !== 1) {
    return { leaders: [], comparable: false };
  }

  const bestValue = Math.min(...values.map((entry) => Number(entry.info.value)));
  return {
    leaders: values
      .filter((entry) => Number(entry.info.value) === bestValue)
      .map((entry) => entry.vehicle),
    comparable: true,
  };
}

function buildDecisionAggregate(vehicles, categories) {
  const scores = new Map();
  const labelsByKey = new Map();

  categories.forEach(({ label, leaders }) => {
    if (!leaders || !leaders.length) return;
    leaders.forEach((vehicle) => {
      const key = getDecisionVehicleKey(vehicle);
      scores.set(key, (scores.get(key) || 0) + 1);
      if (label) {
        const labels = labelsByKey.get(key) || [];
        if (!labels.includes(label)) labels.push(label);
        labelsByKey.set(key, labels);
      }
    });
  });

  const maxScore = Math.max(0, ...scores.values());
  const leaders = maxScore > 0
    ? vehicles.filter((vehicle) => scores.get(getDecisionVehicleKey(vehicle)) === maxScore)
    : [];

  return { leaders, scores, labelsByKey };
}

function getAggregateLeaderLabels(aggregate) {
  if (!aggregate || !aggregate.leaders || !aggregate.leaders.length) return [];
  const labels = [];
  aggregate.leaders.forEach((vehicle) => {
    const key = getDecisionVehicleKey(vehicle);
    (aggregate.labelsByKey.get(key) || []).forEach((label) => {
      if (!labels.includes(label)) labels.push(label);
    });
  });
  return labels;
}

function buildGroupCompareDecisionData(vehicles) {
  const items = (vehicles || []).filter(Boolean);
  if (items.length < 2) return null;

  const powerMeta = getNumericDecisionMeta(items, (vehicle) => vehicle.power, true);
  const accMeta = getNumericDecisionMeta(items, (vehicle) => vehicle.acc, false);
  const topSpeedMeta = getNumericDecisionMeta(items, (vehicle) => vehicle.topSpeed, true);
  const priceMeta = getNumericDecisionMeta(items, (vehicle) => getPriceMeta(vehicle.price).amount, false);
  const yearMeta = getNumericDecisionMeta(items, (vehicle) => extractModelYear(vehicle), true);
  const consumptionMeta = getConsumptionDecisionMeta(items);

  const performanceAggregate = buildDecisionAggregate(items, [
    { label: 'power', leaders: powerMeta.leaders },
    { label: '0-100 km/h', leaders: accMeta.leaders },
    { label: 'top speed', leaders: topSpeedMeta.leaders },
  ]);

  const valueAggregate = buildDecisionAggregate(items, [
    { label: 'price', leaders: priceMeta.leaders },
    { label: 'efficiency', leaders: consumptionMeta.leaders },
    { label: 'model year', leaders: yearMeta.leaders },
  ]);

  const speedAggregate = topSpeedMeta.leaders.length
    ? { leaders: topSpeedMeta.leaders }
    : (accMeta.leaders.length ? { leaders: accMeta.leaders } : { leaders: performanceAggregate.leaders });

  const overallAggregate = buildDecisionAggregate(items, [
    { leaders: powerMeta.leaders },
    { leaders: accMeta.leaders },
    { leaders: topSpeedMeta.leaders },
    { leaders: priceMeta.leaders },
    { leaders: consumptionMeta.leaders },
    { leaders: yearMeta.leaders },
    { leaders: performanceAggregate.leaders },
    { leaders: valueAggregate.leaders },
    { leaders: speedAggregate.leaders },
  ]);

  const performanceLabels = getAggregateLeaderLabels(performanceAggregate);
  const valueLabels = getAggregateLeaderLabels(valueAggregate);

  const verdicts = [
    {
      label: 'Performance winner',
      winner: formatDecisionWinnerNames(performanceAggregate.leaders),
      reason: performanceAggregate.leaders.length
        ? `${performanceAggregate.leaders.length > 1 ? 'Shared lead' : 'Leads'} on ${joinDecisionLabels(performanceLabels)}.`
        : 'No clear edge on the recorded performance data.',
    },
    {
      label: 'Speed winner',
      winner: formatDecisionWinnerNames(speedAggregate.leaders),
      reason: speedAggregate.leaders.length
        ? (
          topSpeedMeta.leaders.length
            ? `${topSpeedMeta.leaders.length > 1 ? 'Share' : 'Has'} the highest top speed on paper.`
            : `${accMeta.leaders.length > 1 ? 'Share' : 'Has'} the quickest acceleration on paper.`
        )
        : 'No clear speed advantage on the recorded data.',
    },
    {
      label: 'Value winner',
      winner: formatDecisionWinnerNames(valueAggregate.leaders),
      reason: valueAggregate.leaders.length
        ? `${valueAggregate.leaders.length > 1 ? 'Shared lead' : 'Stronger'} on ${joinDecisionLabels(valueLabels)}.`
        : 'No clear value edge on price, efficiency, or model year.',
    },
    {
      label: 'Overall winner',
      winner: formatDecisionWinnerNames(overallAggregate.leaders),
      reason: overallAggregate.leaders.length
        ? (
          overallAggregate.leaders.length > 1
            ? 'Share the strongest overall score across the recorded categories.'
            : 'Wins more of the recorded comparison categories overall.'
        )
        : 'The available data is too evenly matched to separate them.',
    },
  ];

  const powerLeaderKeys = new Set(powerMeta.leaders.map(getDecisionVehicleKey));
  const accLeaderKeys = new Set(accMeta.leaders.map(getDecisionVehicleKey));
  const topSpeedLeaderKeys = new Set(topSpeedMeta.leaders.map(getDecisionVehicleKey));
  const priceLeaderKeys = new Set(priceMeta.leaders.map(getDecisionVehicleKey));
  const consumptionLeaderKeys = new Set(consumptionMeta.leaders.map(getDecisionVehicleKey));
  const yearLeaderKeys = new Set(yearMeta.leaders.map(getDecisionVehicleKey));
  const overallLeaderKeys = new Set(overallAggregate.leaders.map(getDecisionVehicleKey));

  const tradeoffs = items.map((vehicle) => {
    const key = getDecisionVehicleKey(vehicle);
    const pros = [];
    const cons = [];

    if (powerMeta.comparable) {
      if (powerLeaderKeys.has(key)) pushUnique(pros, 'Power leader');
      else pushUnique(cons, 'Less power than the group leader');
    }

    if (accMeta.comparable) {
      if (accLeaderKeys.has(key)) pushUnique(pros, 'Quickest 0-100 km/h');
      else pushUnique(cons, 'Slower off the line than the quickest pick');
    }

    if (topSpeedMeta.comparable) {
      if (topSpeedLeaderKeys.has(key)) pushUnique(pros, 'Top speed leader');
      else pushUnique(cons, 'Lower top speed than the fastest pick');
    }

    if (priceMeta.comparable) {
      if (priceLeaderKeys.has(key)) pushUnique(pros, 'Lowest price');
      else pushUnique(cons, 'Higher price than the value leader');
    }

    if (consumptionMeta.comparable) {
      if (consumptionLeaderKeys.has(key)) pushUnique(pros, 'Best efficiency');
      else pushUnique(cons, 'Less efficient than the best option');
    }

    if (yearMeta.comparable) {
      if (yearLeaderKeys.has(key)) pushUnique(pros, 'Newest model year');
      else pushUnique(cons, 'Older model than the newest option');
    }

    if (overallLeaderKeys.has(key)) {
      pushUnique(pros, 'Strong overall spec balance');
    }

    if (!pros.length) pushUnique(pros, 'Competitive overall spec balance');
    if (!cons.length) pushUnique(cons, 'Few clear weaknesses in the recorded specs');

    return {
      title: getDecisionVehicleName(vehicle),
      pros: pros.slice(0, 3),
      cons: cons.slice(0, 3),
    };
  });

  return { verdicts, tradeoffs };
}

function renderCompareDecisionSection() {
  if (!compareDecisionArea || !compareDecisionVerdicts || !compareDecisionTradeoffs) return;
  compareDecisionVerdicts.innerHTML = '';
  compareDecisionTradeoffs.innerHTML = '';

  if (selected.length < 2) {
    compareDecisionArea.classList.add('hidden');
    return;
  }

  const data = buildGroupCompareDecisionData(selected);
  if (!data) {
    compareDecisionArea.classList.add('hidden');
    return;
  }

  data.verdicts.forEach((item) => {
    const card = document.createElement('article');
    card.className = 'compare-decision-verdict';
    card.innerHTML = `
      <div class="section-kicker">${item.label}</div>
      <strong>${item.winner}</strong>
      <p>${item.reason}</p>
    `;
    compareDecisionVerdicts.appendChild(card);
  });

  data.tradeoffs.forEach((group) => {
    const card = document.createElement('article');
    card.className = 'decision-tradeoff-card';
    card.innerHTML = `
      <h3>${group.title}</h3>
      <div class="decision-tradeoff-group">
        <h4>Pros</h4>
        <ul class="decision-tradeoff-list pros">
          ${group.pros.map((item) => `<li>${item}</li>`).join('')}
        </ul>
      </div>
      <div class="decision-tradeoff-group">
        <h4>Cons</h4>
        <ul class="decision-tradeoff-list cons">
          ${group.cons.map((item) => `<li>${item}</li>`).join('')}
        </ul>
      </div>
    `;
    compareDecisionTradeoffs.appendChild(card);
  });

  compareDecisionArea.classList.remove('hidden');
}

function renderComparisonRaceLinks() {
  if (!raceLinksArea || !raceLinksList) return;
  const raceLinks = getComparisonRaceLinks(selected);
  raceLinksList.innerHTML = '';
  if (raceLinks.length === 0) {
    raceLinksArea.classList.add('hidden');
    return;
  }

  raceLinks.forEach(entry => {
    const link = document.createElement('a');
    link.className = 'race-link-card';
    link.href = entry.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';

    const label = document.createElement('span');
    label.className = 'race-link-label';
    label.textContent = entry.title;

    const meta = document.createElement('span');
    meta.className = 'race-link-meta';
    meta.textContent = t('raceLinksSearch');

    link.appendChild(label);
    link.appendChild(meta);
    raceLinksList.appendChild(link);
  });

  raceLinksArea.classList.remove('hidden');
}

// build comparison table with maxima highlighted
function buildTable(options = {}) {
  const { scroll = false } = options;
  if (selected.length === 0) return;

  const maxPower = Math.max(...selected.map(v => Number(v.power || 0)));
  const minAcc = Math.min(...selected.map(v => Number(v.acc || Infinity)));
  const maxTop = Math.max(...selected.map(v => Number(v.topSpeed || 0)));

  compTable.innerHTML = '';

  selected.forEach(v => {
    const tr = document.createElement('tr');

    function td(content, highlight = false, className){
      const td = document.createElement('td');
      if (highlight) td.classList.add('highlight');
      if (className) td.classList.add(className);
      td.innerHTML = content;
      return td;
    }

    const consumptionInfo = getConsumptionInfo(v);
    const consumptionText = consumptionInfo ? `${consumptionInfo.value} ${consumptionInfo.unit}` : '-';
    const computedCost = calculateCost(v);
    const costValue = (v.cost !== undefined && v.cost !== null && v.cost !== '') ? v.cost : computedCost;

    tr.appendChild(td(v.name));
    tr.appendChild(td(v.power, Number(v.power) === maxPower));
    tr.appendChild(td(v.acc, Number(v.acc) === minAcc));
    tr.appendChild(td(v.topSpeed, Number(v.topSpeed) === maxTop));
    tr.appendChild(td(v.engine));
    tr.appendChild(td(formatPrice(v.price) || '-'));
    tr.appendChild(td(consumptionText, false, 'col-consumption'));
    tr.appendChild(td(formatCostValue(costValue), false, 'col-cost'));
    compTable.appendChild(tr);
  });

  if (tableArea) {
    tableArea.classList.remove('hidden');
    if (scroll) {
      tableArea.scrollIntoView({ behavior: 'smooth' });
    }
  }
  setFuelCalculatorVisible(true);
}

// events
const sortButtons = Array.from(document.querySelectorAll('#filterBar button'));
function setSort(sortKey) {
  activeSort = sortKey || null;
  sortButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.sort === activeSort));
  renderList(searchInput ? searchInput.value : '');
}
sortButtons.forEach(btn => {
  btn.addEventListener('click', () => setSort(btn.dataset.sort));
});

function setCatalog(nextCatalog) {
  const next = INVENTORY_MAP[nextCatalog] ? nextCatalog : 'cars';
  activeCatalog = next;
  localStorage.setItem('catalogType', next);
  catalogButtons.forEach(btn => {
    const isActive = btn.dataset.catalog === next;
    btn.classList.toggle('active', isActive);
    btn.setAttribute('aria-selected', isActive);
  });
  activeBrand = brandSelectionByCatalog[activeCatalog] || 'all';
  buildBrandOptions();
  renderList(searchInput ? searchInput.value : '');
  renderSelected();
  applyTranslations();
}

catalogButtons.forEach(btn => {
  btn.addEventListener('click', () => setCatalog(btn.dataset.catalog));
});

setCatalog(activeCatalog);
initFavoritesUI();
renderFavorites();
initNotificationsUI();
initFuelCalculator();

const SEO_PRESELECT = {
  'audi-sq8-2024-fuel-cost': { catalog: 'cars', ids: ['SQ8'] },
  'tesla-model-y-charging-cost': { catalog: 'cars', ids: ['Model Y'] },
  'bmw-m5-fuel-consumption': { catalog: 'cars', ids: ['M5'] },
  'toyota-corolla-fuel-cost': { catalog: 'cars', ids: ['Corolla'] },
  'ford-mustang-mach-e-fuel-cost': { catalog: 'cars', ids: ['Mustang Mach-E'] },
  'lamborghini-aventador-top-speed': { catalog: 'cars', ids: ['Aventador'] },
  'bmw-m5-top-speed': { catalog: 'cars', ids: ['M5'] },
  'bmw-m5-cs-top-speed': { catalog: 'cars', ids: ['M5 CS'] },
  'audi-rs6-top-speed': { catalog: 'cars', ids: ['RS6'] },
  'porsche-911-turbo-top-speed': { catalog: 'cars', ids: ['911'] },
  'mercedes-amg-gt-top-speed': { catalog: 'cars', ids: ['AMG GT'] },
  'audi-rs6-vs-bmw-m5-cs': { catalog: 'cars', ids: ['RS6', 'M5 CS'] },
  'bugatti-chiron-vs-koenigsegg-agera-rs': { catalog: 'cars', ids: ['Chiron', 'Agera RS'] },
  'lamborghini-veneno-vs-ferrari-enzo-ferrari': { catalog: 'cars', ids: ['Veneno', 'Enzo Ferrari'] },
  'mercedes-benz-sls-vs-aston-martin-lagonda': { catalog: 'cars', ids: ['SLS', 'Lagonda'] },
  'pagani-huayra-vs-mclaren-720s': { catalog: 'cars', ids: ['Huayra', '720S'] },
};

function normalizeSeoSlug(pathname) {
  const raw = decodeURIComponent(String(pathname || '')).trim();
  const trimmed = raw.replace(/^\/+|\/+$/g, '');
  if (!trimmed) return '';
  return trimmed
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

function applySeoPreselect() {
  const slug = normalizeSeoSlug(window.location.pathname);
  if (!slug) return;
  const entry = SEO_PRESELECT[slug];
  if (!entry) return;
  const catalog = entry.catalog || 'cars';
  setCatalog(catalog);
  selected = [];
  const source = catalog === 'motorcycles' ? MOTORCYCLES : VEHICLES;
  entry.ids.forEach(id => {
    const veh = source.find(x => String(x.id).toLowerCase() === String(id).toLowerCase());
    if (!veh) return;
    const key = makeKey(catalog, veh.id);
    if (selected.find(s => (s._key || makeKey(s.catalog || catalog, s.id)) === key)) return;
    selected.push({ ...veh, _key: key, catalog });
  });
  renderSelected();
  if (selected.length) buildTable();
}

applySeoPreselect();

searchInput.addEventListener('input', (e) => renderList(e.target.value));
if (brandSelect) {
  brandSelect.addEventListener('change', (e) => {
    activeBrand = e.target.value || 'all';
    brandSelectionByCatalog[activeCatalog] = activeBrand;
    renderList(searchInput ? searchInput.value : '');
  });
}
clearBtn.addEventListener('click', () => { selected = []; renderSelected(); });
compareBtn.addEventListener('click', () => {
  if (selected.length === 0) { alert(t('selectPrompt')); return; }
  buildTable({ scroll: true });
});


// init

// image lightbox for vehicle thumbnails
const imgLightbox = document.createElement('div');
imgLightbox.className = 'img-lightbox';
imgLightbox.innerHTML = `
  <button class=\"close-btn\" aria-label=\"Close image\">?</button>
  <img src=\"\" alt=\"Vehicle image preview\" />
`;
document.body.appendChild(imgLightbox);
const lightboxImg = imgLightbox.querySelector('img');
const closeLightboxBtn = imgLightbox.querySelector('.close-btn');

const openLightbox = (src) => {
  if (!src || !lightboxImg) return;
  lightboxImg.src = src;
  imgLightbox.classList.add('show');
};

const closeLightbox = () => imgLightbox.classList.remove('show');

if (closeLightboxBtn) closeLightboxBtn.addEventListener('click', closeLightbox);
imgLightbox.addEventListener('click', (e) => {
  if (e.target === imgLightbox) closeLightbox();
});

const themeToggle = document.getElementById('themeToggle');
const storedTheme = localStorage.getItem('theme');
const isLocalHost = ['127.0.0.1', 'localhost'].includes(window.location.hostname);
const defaultDark = isLocalHost ? true : (storedTheme ? storedTheme === 'dark' : true);

const syncTheme = (forceDark) => {
  const next = typeof forceDark === 'boolean' ? forceDark : document.body.classList.contains('dark');
  document.body.classList.toggle('dark', next);
  if (themeToggle) themeToggle.checked = next;
  localStorage.setItem('theme', next ? 'dark' : 'light');
};

document.body.classList.toggle('dark', defaultDark);

if (themeToggle) {
  syncTheme(defaultDark);
  themeToggle.addEventListener('change', (e) => {
    syncTheme(e.target.checked);
  });
} else {
  syncTheme(defaultDark);
}

// Language dropdown + translations
let langToggleBtn = null;

function applyTranslations() {
  const pack = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const sidebarTitle = document.querySelector('.sidebar-header h2');
  if (sidebarTitle) sidebarTitle.textContent = activeCatalog === 'motorcycles'
    ? (pack.motorcyclesTitle || pack.vehiclesTitle)
    : pack.vehiclesTitle;
  document.querySelectorAll('#catalogToggle button').forEach(btn => {
    const key = btn.dataset.catalog === 'motorcycles' ? 'catalogMotorcycles' : 'catalogCars';
    if (pack[key]) btn.textContent = pack[key];
  });
  if (searchInput) searchInput.placeholder = pack.searchPlaceholder;
  const brandLabel = document.querySelector('.brand-label');
  if (brandLabel) brandLabel.textContent = pack.brandLabel || 'Brand';
  if (brandSelect) buildBrandOptions();
  document.querySelectorAll('#filterBar button').forEach(btn => {
    const key = btn.dataset.sort || btn.dataset.type;
    if (pack.filters && pack.filters[key]) btn.textContent = pack.filters[key];
  });
  const mainTitle = document.querySelector('.main-header h1');
  if (mainTitle) mainTitle.textContent = pack.comparison;
  if (clearBtn) clearBtn.textContent = pack.clear;
  if (compareBtn) compareBtn.textContent = pack.compare;
  const tableTitle = document.querySelector('#tableArea h2');
  if (tableTitle) tableTitle.textContent = pack.tableTitle;
  const tableHeaders = document.querySelectorAll('#compTable thead th');
  if (tableHeaders.length && Array.isArray(pack.tableHeaders)) {
    tableHeaders.forEach((th, idx) => {
      if (pack.tableHeaders[idx]) th.textContent = pack.tableHeaders[idx];
    });
  }
  const fuelTitle = document.getElementById('fuelCalcTitle');
  if (fuelTitle) fuelTitle.textContent = pack.costTitle;
  const fuelDistanceLabel = document.getElementById('fuelCalcDistanceLabel');
  if (fuelDistanceLabel) fuelDistanceLabel.textContent = pack.distanceLabel;
  updateFuelCalcLabels();
  const fuelResultLabel = document.getElementById('fuelCalcResultLabel');
  if (fuelResultLabel) fuelResultLabel.textContent = pack.costEstimate;
  updateFuelPremiumUi();
  const commentsTitle = document.querySelector('.comment-section h3');
  if (commentsTitle) commentsTitle.textContent = pack.commentsTitle;
  const usernameInput = document.getElementById('username');
  if (usernameInput) usernameInput.placeholder = pack.commentName;
  const commentInput = document.getElementById('commentInput');
  if (commentInput) commentInput.placeholder = pack.commentPlaceholder;
  const ratingLabel = document.querySelector('label[for="rating"]');
  if (ratingLabel) ratingLabel.textContent = pack.ratingLabel;
  const submitBtn = document.querySelector('#commentForm button[type="submit"]');
  if (submitBtn) submitBtn.textContent = pack.submit;
  const loginBtnEl = document.getElementById('loginBtn');
  if (loginBtnEl) loginBtnEl.textContent = pack.login;
  const formTitleEl = document.getElementById('formTitle');
  if (formTitleEl) formTitleEl.textContent = pack.login;
  if (notificationsBtn) {
    const notificationsLabel = pack.notificationsTitle || 'Notifications';
    notificationsBtn.setAttribute('aria-label', notificationsLabel);
    notificationsBtn.setAttribute('title', notificationsLabel);
  }
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (pack[key]) el.textContent = pack[key];
  });
  renderNotifications();
}

function setLanguage(code) {
  const langObj = getLang(code) || LANGUAGES[0];
  currentLang = langObj.code;
  localStorage.setItem('appLang', currentLang);
  if (langToggleBtn) {
    const labelEl = langToggleBtn.querySelector('.lang-label');
    if (labelEl) labelEl.textContent = langObj.label;
  }
  renderList();
  renderSelected();
  applyTranslations();
  if (fuelCalcSection) {
    loadFuelInputsForUnit(getFuelUnit());
    updateFuelCalculator();
  }
  renderFavorites();
  document.dispatchEvent(new CustomEvent('languagechange', { detail: langObj }));
}

function initLanguageMenu() {
  const sidebarHost = document.querySelector('.sidebar-header');
  let host = null;

  // Prefer placing near main title; fall back to sidebar, then auth/topbar
  const mainHeader = document.querySelector('.main-header');
  if (mainHeader) {
    let leftGroup = mainHeader.querySelector('.main-header-left');
    if (!leftGroup) {
      leftGroup = document.createElement('div');
      leftGroup.className = 'main-header-left';
      const title = mainHeader.querySelector('h1');
      if (title) {
        mainHeader.insertBefore(leftGroup, title);
        leftGroup.appendChild(title);
      } else {
        mainHeader.prepend(leftGroup);
      }
    }
    host = leftGroup;
  } else if (sidebarHost) {
    host = sidebarHost;
  } else {
    host = authArea || topbarEl;
  }
  if (!host) return;

  const wrapper = document.createElement('div');
  wrapper.className = 'lang-wrapper';
  if (host === sidebarHost) {
    wrapper.classList.add('lang-sidebar');
  }

  const toggleBtn = document.createElement('button');
  langToggleBtn = toggleBtn;
  toggleBtn.type = 'button';
  toggleBtn.className = 'lang-toggle';
  const initialLang = getLang(currentLang) || LANGUAGES[0];
  toggleBtn.innerHTML = `<span class="lang-label">${initialLang.label}</span><span class="lang-caret">&#9662;</span>`;

  const menu = document.createElement('div');
  menu.className = 'lang-menu';
  menu.setAttribute('role', 'menu');

  const closeMenu = () => {
    menu.classList.remove('open');
    toggleBtn.classList.remove('open');
  };

  const renderOptions = () => {
    menu.innerHTML = '';
    LANGUAGES.forEach(lang => {
      const opt = document.createElement('button');
      opt.type = 'button';
      opt.className = `lang-option${lang.code === currentLang ? ' active' : ''}`;
      opt.dataset.code = lang.code;
      opt.innerHTML = `<span class="dot"></span><span>${lang.label}</span>`;
      opt.addEventListener('click', () => {
        if (lang.code === currentLang) {
          closeMenu();
          return;
        }
        setLanguage(lang.code);
        renderOptions();
        closeMenu();
      });
      menu.appendChild(opt);
    });
  };

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const willOpen = !menu.classList.contains('open');
    document.querySelectorAll('.lang-menu.open').forEach(m => m.classList.remove('open'));
    document.querySelectorAll('.lang-toggle.open').forEach(t => t.classList.remove('open'));
    if (willOpen) {
      menu.classList.add('open');
      toggleBtn.classList.add('open');
    } else {
      closeMenu();
    }
  });

  document.addEventListener('click', (e) => {
    if (!wrapper.contains(e.target)) {
      closeMenu();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });

  const vehicleToggleBtn = document.createElement('button');
  vehicleToggleBtn.type = 'button';
  vehicleToggleBtn.className = 'mobile-panel-toggle';
  vehicleToggleBtn.hidden = true;
  vehicleToggleBtn.addEventListener('click', () => {
    const nextCollapsed = !document.body.classList.contains('mobile-sidebar-collapsed');
    setMobileSidebarCollapsed(nextCollapsed);
  });
  mobileVehicleToggleBtn = vehicleToggleBtn;

  wrapper.appendChild(toggleBtn);
  wrapper.appendChild(vehicleToggleBtn);
  wrapper.appendChild(menu);
  host.prepend(wrapper);
  renderOptions();
  updateMobileVehicleToggle();
}

initLanguageMenu();
setLanguage(currentLang);
syncMobileViewportLayout();
window.addEventListener('resize', () => {
  if (!isMobileSplitLayout()) {
    document.body.classList.remove('mobile-sidebar-collapsed');
  }
  syncMobileViewportLayout();
  updateMobileVehicleToggle();
});



// Comment
(function(){
  const form = document.getElementById("commentForm");
  const container = document.getElementById("commentsContainer");
  const usernameInput = document.getElementById("username");
  const commentInput = document.getElementById("commentInput");
  const ratingInput = document.getElementById("rating");
  if (!form || !container || !usernameInput || !commentInput || !ratingInput) return;

  const currentUser = (window.currentUser && window.currentUser.email) ? window.currentUser : null;
  const currentUserId = currentUser ? (currentUser.email || currentUser.name || "anon") : null;
  const commentsApiUrl = "/api/comments";
  let comments = [];
  let loginNote = document.getElementById("loginToCommentNote");

  const escapeHtml = (value) => String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
  const formatStars = (rating) => "\u2605".repeat(Math.max(0, Math.min(5, rating))) + "\u2606".repeat(Math.max(0, 5 - Math.max(0, Math.min(5, rating))));

  const ensureShape = (c) => {
    let changed = false;
    if (!c.id) { c.id = `c_${Date.now()}_${Math.random().toString(16).slice(2)}`; changed = true; }
    if (typeof c.likes === "number") { c.likes = []; changed = true; }
    if (!Array.isArray(c.likes)) { c.likes = []; changed = true; }
    if (!Array.isArray(c.dislikes)) { c.dislikes = []; changed = true; }
    if (!Array.isArray(c.replies)) { c.replies = []; changed = true; }
    if (!c.username) { c.username = "User"; changed = true; }
    if (!c.date) { c.date = new Date().toLocaleDateString("en-GB"); changed = true; }
    if (!Number.isInteger(c.rating) || c.rating < 1 || c.rating > 5) { c.rating = 5; changed = true; }
    return [c, changed];
  };

  function syncComments(nextComments) {
    comments = Array.isArray(nextComments)
      ? nextComments.map((comment) => ensureShape(comment)[0])
      : [];
  }

  function renderComments() {
    container.innerHTML = "";
    comments.forEach((c, i) => {
      ensureShape(c);
      const div = document.createElement("div");
      div.className = "comment";

      const stars = formatStars(c.rating);
      const safeUsername = escapeHtml(c.username);
      const safeDate = escapeHtml(c.date);
      const safeText = escapeHtml(c.text);
      const avatarLetter = (c.username || "U").trim().slice(0, 1).toUpperCase() || "U";

      div.innerHTML = `
        <div class="comment-header">
          <div class="comment-avatar">${avatarLetter}</div>
          <div class="comment-meta">
            <span class="comment-name">${safeUsername}</span>
            <span>${safeDate}</span>
          </div>
        </div>
        <div class="comment-rating">${stars}</div>
        <div class="comment-body">${safeText}</div>
        <div class="comment-actions">
          <button class="icon-btn" data-action="like" data-id="${c.id}">Like (${c.likes.length})</button>
          <button class="icon-btn" data-action="reply" data-id="${c.id}">Reply</button>
        </div>
        <div class="reply-list" id="replies-${c.id}">
          ${c.replies.map(r => `
            <div class="reply">
              <div class="comment-header">
                <span>${escapeHtml(r.username)}</span>
                <span>${escapeHtml(r.date)}</span>
              </div>
              <div class="comment-body">${escapeHtml(r.text)}</div>
            </div>
          `).join('')}
        </div>
      `;
      container.appendChild(div);
    });

    if (!comments.length) {
      container.innerHTML = `<p>No comments yet.</p>`;
    }
  }

  async function fetchComments() {
    const response = await fetch(commentsApiUrl, {
      headers: { "Accept": "application/json" }
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || !data.ok) {
      throw new Error(data.message || "Comments could not be loaded.");
    }
    syncComments(data.comments);
    renderComments();
    return data.comments;
  }

  function setFormState(isSubmitting) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (!submitBtn) return;
    submitBtn.disabled = isSubmitting;
  }

  if (!currentUser) {
    form.style.display = "none";
    if (!loginNote) {
      container.insertAdjacentHTML(
        "beforebegin",
        `<p id="loginToCommentNote" data-i18n="loginToComment">${t('loginToComment')}</p>`
      );
      loginNote = document.getElementById("loginToCommentNote");
    }
  } else {
    if (usernameInput) {
      usernameInput.value = currentUser.name || currentUser.email || "User";
      usernameInput.readOnly = true;
    }
    form.style.display = "flex";
    if (loginNote) loginNote.remove();
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = commentInput.value.trim();
    const rating = parseInt(ratingInput.value);

    if (text.length < 10 || text.length > 500) {
      alert("Comment must be between 10 and 500 characters.");
      return;
    }

    try {
      setFormState(true);
      const response = await fetch(commentsApiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, rating })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) {
        throw new Error(data.message || "Comment could not be saved.");
      }
      syncComments(data.comments);
      renderComments();
      form.reset();
      if (usernameInput) {
        usernameInput.value = currentUser ? (currentUser.name || currentUser.email || "User") : "";
      }
    } catch (error) {
      alert(error.message || "Comment could not be saved.");
    } finally {
      setFormState(false);
    }
  });

  container.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;
    const action = btn.dataset.action;
    const id = btn.dataset.id;
    const userId = currentUserId;
    if (!userId) {
      alert("Please log in to interact with comments.");
      return;
    }
    const idx = comments.findIndex(c => c.id === id);
    if (idx === -1) return;
    const [comment] = ensureShape(comments[idx]);

    if (action === "like") {
      try {
        const response = await fetch(`${commentsApiUrl}/${encodeURIComponent(id)}/like`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.ok) {
          throw new Error(data.message || "Like action failed.");
        }
        syncComments(data.comments);
        renderComments();
      } catch (error) {
        alert(error.message || "Like action failed.");
      }
      return;
    }

    if (action === "reply") {
      const replyText = prompt("Reply:");
      if (!replyText || replyText.trim().length === 0) return;
      try {
        const response = await fetch(`${commentsApiUrl}/${encodeURIComponent(id)}/replies`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: replyText.trim() })
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.ok) {
          throw new Error(data.message || "Reply could not be saved.");
        }
        syncComments(data.comments);
        renderComments();
      } catch (error) {
        alert(error.message || "Reply could not be saved.");
      }
    }
  });

  fetchComments().catch((error) => {
    container.innerHTML = `<p>${escapeHtml(error.message || "Comments could not be loaded.")}</p>`;
  });
})();

// Load existing comments
// Open popup
const loginBtn = document.getElementById("loginBtn");
const loginModal = document.getElementById("loginModal");
const authForm = document.getElementById("authForm");
const promoVideo = document.querySelector(".promo-video");
const loginName = document.getElementById("loginName");
const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");
const togglePassword = document.getElementById("togglePassword");
const formTitle = document.getElementById("formTitle");
const toggleAuthMode = document.getElementById("toggleAuthMode");
const toggleCopyText = document.getElementById("toggleCopyText");
const forgotLink = document.getElementById("forgotLink");
const submitBtn = document.getElementById("submitBtn");
const authError = document.getElementById("authError");
const strengthLabel = document.getElementById("strengthLabel");
const verificationCodeInput = document.getElementById("verificationCode");
const codeBlock = document.getElementById("codeBlock");
const codeHint = document.getElementById("codeHint");
const resendCodeBtn = document.getElementById("resendCode");
let authMode = "login";
let signupStage = "start"; // start -> verify
let pendingSignupPayload = null;
let resetStage = "idle"; // idle -> start -> verify

const ensurePromoVideoLoaded = () => {
  if (!promoVideo) return;
  const dataSrc = promoVideo.getAttribute("data-src");
  if (dataSrc && !promoVideo.getAttribute("src")) {
    promoVideo.setAttribute("src", dataSrc);
    promoVideo.load();
  }
  const playPromise = promoVideo.play();
  if (playPromise && typeof playPromise.catch === "function") {
    playPromise.catch(() => {});
  }
};

const stopPromoVideo = () => {
  if (!promoVideo) return;
  promoVideo.pause();
};

const openLoginModal = () => {
  if (!loginModal) return;
  loginModal.style.display = "block";
  ensurePromoVideoLoaded();
};

const closeLoginModal = () => {
  if (!loginModal) return;
  loginModal.style.display = "none";
  stopPromoVideo();
};

const resetSignupFlow = () => {
  signupStage = "start";
  pendingSignupPayload = null;
   // reset flow state
  resetStage = authMode === "reset" ? "start" : "idle";
  if (verificationCodeInput) {
    verificationCodeInput.value = "";
    verificationCodeInput.classList.add("hidden");
  }
  if (codeBlock) codeBlock.classList.add("hidden");
  if (codeHint) codeHint.classList.add("hidden");
  if (resendCodeBtn) resendCodeBtn.classList.add("hidden");
  if (loginEmail) loginEmail.readOnly = false;
  if (loginName) loginName.readOnly = false;
  if (loginPassword) loginPassword.readOnly = false;
  if (loginPassword) loginPassword.placeholder = authMode === "reset" ? "New password" : "Password";
  if (submitBtn) {
    submitBtn.textContent =
      authMode === "login" ? "Log In" : authMode === "reset" ? "Send Code" : "Create Account";
  }
};

if (loginBtn && loginModal) {
  loginBtn.addEventListener("click", openLoginModal);

  window.addEventListener("click", (e) => {
    if (e.target === loginModal) {
      closeLoginModal();
    }
  });
}

const setAuthMode = (mode) => {
  authMode = mode;
  if (formTitle) {
    formTitle.textContent = mode === "login" ? "Log In" : mode === "reset" ? "Reset Password" : "Create Account";
  }
  if (submitBtn) {
    submitBtn.textContent = mode === "login" ? "Log In" : mode === "reset" ? "Send Code" : "Create Account";
  }
  if (toggleAuthMode) {
    toggleAuthMode.textContent = mode === "login" ? "Create one" : "Back to login";
  }
  if (toggleCopyText) {
    toggleCopyText.textContent =
      mode === "login"
        ? "Don't have an account?"
        : mode === "reset"
        ? "Remembered your password?"
        : "Have an account?";
  }
  if (loginName) loginName.classList.toggle("hidden", mode !== "signup");
  if (authError) authError.classList.add("hidden");
  resetSignupFlow();
};

if (toggleAuthMode) {
  toggleAuthMode.addEventListener("click", (e) => {
    e.preventDefault();
    if (authMode === "reset") {
      setAuthMode("login");
    } else {
      setAuthMode(authMode === "login" ? "signup" : "login");
    }
  });
}

if (togglePassword && loginPassword) {
  togglePassword.addEventListener("click", () => {
    const isText = loginPassword.type === "text";
    loginPassword.type = isText ? "password" : "text";
    togglePassword.classList.toggle("showing", !isText);
    togglePassword.setAttribute("aria-label", isText ? "Show password" : "Hide password");
    togglePassword.title = isText ? "Show password" : "Hide password";
  });
  togglePassword.classList.toggle("showing", loginPassword.type === "text");
}

function computeStrength(pw) {
  let score = 0;
  if (pw.length >= 8) score++;
  if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++;
  if (/\d/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;
  if (pw.length >= 12) score++;
  if (score >= 4) return "strong";
  if (score >= 2) return "medium";
  return "weak";
}

function updateStrength() {
  if (!strengthLabel) return;
  const pw = loginPassword ? loginPassword.value : "";
  const strength = computeStrength(pw);
  strengthLabel.classList.remove("strength-weak", "strength-medium", "strength-strong");
  strengthLabel.textContent = `Password strength: ${strength}`;
  strengthLabel.classList.add(`strength-${strength}`);
}

if (loginPassword) {
  loginPassword.addEventListener("input", updateStrength);
}

if (authForm) {
  authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (authError) authError.classList.add("hidden");
    const payload = {
      email: (loginEmail?.value || "").trim(),
      password: loginPassword?.value || "",
    };
    const requirePasswordCheck = authMode !== "reset" || resetStage === "verify";
    if (requirePasswordCheck && payload.password.length < 8) {
      if (authError) {
        authError.textContent = "Password must be at least 8 characters.";
        authError.classList.remove("hidden");
      }
      return;
    }
    if (authMode === "signup") {
      payload.name = (loginName?.value || "").trim();
    }
    try {
      if (authMode === "login") {
        const res = await fetch("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok || !data.ok) {
          if (authError) {
            authError.textContent = data.message || "Something went wrong.";
            authError.classList.remove("hidden");
          } else {
            alert(data.message || "Something went wrong.");
          }
          return;
        }
        window.location.reload();
        return;
      }

      if (authMode === "reset") {
        if (resetStage === "start") {
          if (!payload.email) {
            if (authError) {
              authError.textContent = "Please enter your email to reset.";
              authError.classList.remove("hidden");
            }
            return;
          }
          const res = await fetch("/auth/forgot/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: payload.email }),
          });
          const data = await res.json();
          resetStage = "verify";
          if (submitBtn) submitBtn.textContent = "Verify Code";
          if (codeBlock) codeBlock.classList.remove("hidden");
          if (verificationCodeInput) verificationCodeInput.classList.remove("hidden");
          if (codeHint) {
            codeHint.textContent = "Enter the 6-digit code sent to your email to reset your password.";
            codeHint.classList.remove("hidden");
          }
          if (resendCodeBtn) resendCodeBtn.classList.remove("hidden");
          if (loginEmail) loginEmail.readOnly = true;
          let successMsg = "Reset code sent.";
          if (data.send_error) {
            successMsg = "Code generated but email failed to send.";
          }
          if (authError) {
            authError.textContent = data.message || successMsg;
            authError.classList.remove("hidden");
          } else {
            alert(data.message || successMsg);
          }
          return;
        }

        if (resetStage === "verify") {
          const code = (verificationCodeInput?.value || "").trim();
          if (!code) {
            if (authError) {
              authError.textContent = "Please enter the reset code.";
              authError.classList.remove("hidden");
            }
            return;
          }
          const res = await fetch("/auth/forgot/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: payload.email, code, new_password: payload.password }),
          });
          const data = await res.json();
          if (!res.ok || !data.ok) {
            if (authError) {
              authError.textContent = data.message || "Invalid code.";
              authError.classList.remove("hidden");
            } else {
              alert(data.message || "Invalid code.");
            }
            return;
          }
          window.location.reload();
          return;
        }
      }

      if (signupStage === "start") {
        pendingSignupPayload = payload;
        const res = await fetch("/auth/signup/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok || !data.ok) {
          if (authError) {
            authError.textContent = data.message || "Something went wrong.";
            authError.classList.remove("hidden");
          } else {
            alert(data.message || "Something went wrong.");
          }
          return;
        }
        signupStage = "verify";
        if (submitBtn) submitBtn.textContent = "Verify Code";
        if (codeBlock) codeBlock.classList.remove("hidden");
        if (verificationCodeInput) verificationCodeInput.classList.remove("hidden");
        if (codeHint) codeHint.classList.remove("hidden");
        if (resendCodeBtn) resendCodeBtn.classList.remove("hidden");
        if (loginEmail) loginEmail.readOnly = true;
        if (loginName) loginName.readOnly = true;
        if (loginPassword) loginPassword.readOnly = true;
        let successMsg = "Code sent.";
        if (data.send_error) {
          successMsg = "Code generated but email failed to send.";
        }
        if (authError) {
          authError.textContent = successMsg;
          authError.classList.remove("hidden");
        } else {
          alert(successMsg);
        }
        return;
      }

      if (signupStage === "verify") {
        const code = (verificationCodeInput?.value || "").trim();
        if (!code) {
          if (authError) {
            authError.textContent = "Please enter the verification code.";
            authError.classList.remove("hidden");
          }
          return;
        }
        const res = await fetch("/auth/signup/verify", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: payload.email, code }),
        });
        const data = await res.json();
        if (!res.ok || !data.ok) {
          if (authError) {
            authError.textContent = data.message || "Invalid code.";
            authError.classList.remove("hidden");
          } else {
            alert(data.message || "Invalid code.");
          }
          if (data.message && data.message.toLowerCase().includes("no verification pending")) {
            resetSignupFlow();
          }
          return;
        }
        window.location.reload();
      }
    } catch (err) {
      if (authError) {
        authError.textContent = "Network error. Please try again.";
        authError.classList.remove("hidden");
      } else {
        alert("Network error. Please try again.");
      }
    }
  });
}

if (forgotLink) {
  forgotLink.addEventListener("click", (e) => {
    e.preventDefault();
    setAuthMode("reset");
    if (authError) {
      authError.textContent = "Enter your email to get a reset code.";
      authError.classList.remove("hidden");
    }
  });
}

setAuthMode("login");

if (resendCodeBtn) {
  resendCodeBtn.addEventListener("click", async () => {
    try {
      if (authMode === "signup" && pendingSignupPayload) {
        const res = await fetch("/auth/signup/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(pendingSignupPayload),
        });
        const data = await res.json();
        if (!res.ok || !data.ok) {
          if (authError) {
            authError.textContent = data.message || "Unable to resend code.";
            authError.classList.remove("hidden");
          }
          return;
        }
        let successMsg = "Code sent.";
        if (data.send_error) {
          successMsg = "Code generated but email failed to send.";
        }
        if (authError) {
          authError.textContent = successMsg;
          authError.classList.remove("hidden");
        } else {
          alert(successMsg);
        }
      } else if (authMode === "reset" && loginEmail?.value) {
        const res = await fetch("/auth/forgot/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: loginEmail.value.trim() }),
        });
        const data = await res.json();
        let successMsg = "Reset code sent.";
        if (data.send_error) {
          successMsg = "Code generated but email failed to send.";
        }
        if (!res.ok || !data.ok) {
          if (authError) {
            authError.textContent = data.message || "Unable to resend code.";
            authError.classList.remove("hidden");
          }
          return;
        }
        if (authError) {
          authError.textContent = data.message || successMsg;
          authError.classList.remove("hidden");
        } else {
          alert(data.message || successMsg);
        }
      }
    } catch (err) {
      if (authError) {
        authError.textContent = "Network error. Please try again.";
        authError.classList.remove("hidden");
      }
    }
  });
}

const profileTrigger = document.getElementById("profileMenuTrigger");
const profileMenu = document.getElementById("profileMenu");
const logoutBtn = document.getElementById("logoutBtn");

if (profileTrigger && profileMenu) {
  profileTrigger.addEventListener("click", (e) => {
    e.stopPropagation();
    profileMenu.classList.toggle("open");
  });

  document.addEventListener("click", (e) => {
    if (!profileMenu.contains(e.target) && e.target !== profileTrigger) {
      profileMenu.classList.remove("open");
    }
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    window.location.href = "/logout";
  });
}

