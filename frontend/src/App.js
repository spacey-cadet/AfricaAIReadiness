import React, { useState, useEffect } from 'react';
import './App.css';

const metrics = [
  {
    name: 'InternetPenetration_Percent',
    title: 'Internet Penetration',
    description: 'The percentage of population with internet access, a crucial foundation for AI adoption.'
  },
  {
    name: 'MobilePhoneUsage_SubscriptionsPer100',
    title: 'Mobile Phone Usage',
    description: 'Mobile subscriptions per 100 people, indicating digital connectivity potential.'
  },
  {
    name: 'BroadbandAccess_FixedSubscriptionsPer100',
    title: 'Broadband Access',
    description: 'Fixed broadband subscriptions per 100 people, showing infrastructure readiness.'
  }
];

function App() {
  const [currentMetric, setCurrentMetric] = useState(metrics[0].name);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleMetricChange = (metricName) => {
    setCurrentMetric(metricName);
  };

  const currentMetricData = metrics.find(m => m.name === currentMetric);

  return (
    <div className="app">
      <div className="foggy-background"></div>
      <div className="content">
        <h1 className={`title ${isVisible ? 'visible' : ''}`}>
          Africa Central: AI Readiness Dashboard
        </h1>
        
        <div className={`metric-selector ${isVisible ? 'visible' : ''}`}>
          {metrics.map((metric) => (
            <button
              key={metric.name}
              className={`metric-button ${currentMetric === metric.name ? 'active' : ''}`}
              onClick={() => handleMetricChange(metric.name)}
              aria-label={`View ${metric.title} data`}
            >
              {metric.title}
            </button>
          ))}
        </div>

        <div className={`chart-container ${isVisible ? 'visible' : ''}`}>
          <iframe
            src={`/plots/${currentMetric.toLowerCase()}.html`}
            title={`${currentMetric} Chart`}
            className="chart-frame"
            loading="lazy"
          />
        </div>

        <div className={`description ${isVisible ? 'visible' : ''}`}>
          <h2>{currentMetricData.title}</h2>
          <p>{currentMetricData.description}</p>
        </div>
      </div>
    </div>
  );
}

export default App; 