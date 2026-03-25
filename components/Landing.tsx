import React from 'react';
import { useNavigate } from 'react-router-dom';

const Landing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">🔥</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">BurnCare AI</span>
            </div>
            <div className="space-x-4">
              <button
                onClick={() => navigate('/login')}
                className="px-6 py-2 text-gray-700 hover:text-blue-600 font-medium"
              >
                Login
              </button>
              <button
                onClick={() => navigate('/signup')}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-4 py-24">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            BurnCare AI
          </h1>
          <p className="text-2xl text-blue-600 font-semibold mb-6">
            Smart Decision Support System for Burn Centers
          </p>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Real-time AI-powered mortality risk prediction using LSTM neural networks. 
            Empowering healthcare teams to make informed decisions for better patient outcomes.
          </p>
          <button
            onClick={() => navigate('/signup')}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg"
          >
            Start Now
          </button>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">AI-Powered Predictions</h3>
            <p className="text-gray-600">
              Advanced LSTM models predict mortality risk in real-time based on vital signs and patient data.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Real-Time Monitoring</h3>
            <p className="text-gray-600">
              Continuous patient monitoring with dynamic risk assessment and alerting systems.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition">
            <div className="text-4xl mb-4">👥</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Team Collaboration</h3>
            <p className="text-gray-600">
              Designed for multi-role teams: Doctors, Nurses, and Administrators working together.
            </p>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid md:grid-cols-4 gap-8 mt-16 text-center">
          <div>
            <div className="text-4xl font-bold text-blue-600">24/7</div>
            <p className="text-gray-600">Continuous Monitoring</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600">99%</div>
            <p className="text-gray-600">Accuracy Rate</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600">Real-Time</div>
            <p className="text-gray-600">Risk Assessment</p>
          </div>
          <div>
            <div className="text-4xl font-bold text-blue-600">5 Roles</div>
            <p className="text-gray-600">Role-Based Access</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-blue-900 text-white mt-24">
        <div className="max-w-6xl mx-auto px-4 py-12 text-center">
          <p className="text-blue-200">
            © 2026 BurnCare AI. Advanced healthcare decision support system.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;