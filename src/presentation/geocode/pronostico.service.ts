
import axios from 'axios';
import { envs } from '../../config/envs';
import { GeocodeEntity } from '../../domain/entities/geocode.entity';
import { PronosticoEntity, WeatherData } from '../../domain/entities/pronostico.entity';


const https = require('https');

const agent = new https.Agent({ 
  rejectUnauthorized: false
});

export class PronosticoService {

async getWeather5days(geocode : GeocodeEntity): Promise<any> {
    try {
      const response = await axios.get(`${envs.WEATHER_API_BASE_URL}`, {
        params: {
          lat: geocode.latitude,
          lon: geocode.longitude,
          appid: envs.WEATHER_API_KEY
        },
        httpsAgent: agent
      });
      return response.data;
    } catch (error) {
      return error;
    }
  };


    public cleanWeatherData(data: any): PronosticoEntity[] {
    const pronosticos: PronosticoEntity[] = [];
    
    const weatherXData: { [key: string]: { maxTemperature: number, minTemperature: number, weather: WeatherData }[] } = {};

    data.list.forEach((pronostico: any) => {
      const date = new Date(pronostico.dt * 1000).toISOString().split('T')[0];
      const maxTemperature = parseFloat(pronostico.main.temp_max) - 273.15; 
      const minTemperature = parseFloat(pronostico.main.temp_min) - 273.15;
      const weather: WeatherData = {
        id: pronostico.weather[0].id,
        main: pronostico.weather[0].main,
        description: pronostico.weather[0].description
      };    
      

      if (!weatherXData[date]) {
          weatherXData[date] = [];
        }

      weatherXData[date].push({
        maxTemperature: maxTemperature,
        minTemperature: minTemperature,
        weather: weather});
    });

    Object.entries(weatherXData).forEach(([day, results]) => {
      const maxTemperature = Math.max(...results.map(temp => temp.maxTemperature));
      const minTemperature = Math.min(...results.map(temp => temp.minTemperature));
      
    const weatherCount: { [key: string]: { count: number; weather: WeatherData } } = {};

    results.forEach(({ weather }) => {
        const key = `${weather.id}-${weather.main}-${weather.description}`;
        if (!weatherCount[key]) {
            weatherCount[key] = { count: 0, weather };
        }
        weatherCount[key].count++;
    });


    const mostFrequentWeather = Object.values(weatherCount).reduce((a, b) =>
        a.count > b.count ? a : b
    ).weather;
      pronosticos.push(
        PronosticoEntity.fromObject({
          date: new Date(Date.parse(day)),
          maxTemperature: maxTemperature.toFixed(2),
          minTemperature: minTemperature.toFixed(2),
          weather: mostFrequentWeather
        })
      );
    });
    return pronosticos;
  };
  
}

