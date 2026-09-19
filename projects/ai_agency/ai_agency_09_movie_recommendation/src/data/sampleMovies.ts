import { Movie } from '../types/movie';

export const getSampleRecommendations = (query: string): Movie[] => {
  // This would be replaced with actual API calls to the Flask backend
  return [
    {
      id: '1',
      title: 'Inception',
      year: 2010,
      posterUrl: 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&w=500',
      summary: 'A skilled thief with the rare ability to steal secrets from people\'s minds while they dream must plant an idea into a CEO\'s mind. A complex heist movie that explores dreams within dreams.',
    },
    {
      id: '2',
      title: 'The Matrix',
      year: 1999,
      posterUrl: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=500',
      summary: 'A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to overthrow them. A groundbreaking sci-fi that questions the nature of reality.',
    },
    {
      id: '3',
      title: 'Interstellar',
      year: 2014,
      posterUrl: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?auto=format&fit=crop&w=500',
      summary: 'In a future where Earth is becoming uninhabitable, a team of astronauts travels through a wormhole in search of a new home for humanity. An epic space odyssey about love, time, and survival.',
    },
    {
      id: '4',
      title: 'Blade Runner 2049',
      year: 2017,
      posterUrl: 'https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=500',
      summary: 'A young blade runner discovers a long-buried secret that leads him on a quest to find Rick Deckard, a former blade runner who\'s been missing for 30 years.',
    },
    {
      id: '5',
      title: 'Dune',
      year: 2021,
      posterUrl: 'https://images.unsplash.com/photo-1630839437035-dac17da580d0?auto=format&fit=crop&w=500',
      summary: 'Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, must travel to the most dangerous planet in the universe to ensure the future of his family and his people.',
    },
  ];
};