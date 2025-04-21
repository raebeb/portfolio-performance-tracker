import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const PortfolioChart = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);

    //TODO: make this dynamic when is working
    const portfolioId = 2;
    const fechaInicio = '2022-03-08';
    const fechaFin = '2022-03-20';

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(
                    `http://localhost:8000/api/portfolios/${portfolioId}/summary/?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`
                );
                console.log(response);
                const data = await response.json();
                console.log(data)

                const latest = data[data.length - 1]; // último día
                const weights = latest.weights;
                const labels = Object.keys(weights);
                const values = Object.values(weights).map(Number);

                setChartData({
                    labels: labels,
                    datasets: [
                        {
                            label: 'Peso en Portafolio',
                            data: values,
                            backgroundColor: labels.map((_, i) =>
                                `hsl(${i * 30}, 70%, 60%)`
                            ),
                            borderWidth: 1,
                        },
                    ],
                });

                setLoading(false);
            } catch (error) {
                console.error('Error al obtener los datos:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            <h2>Distribución del Portafolio</h2>
            {loading ? <p>Cargando datos...</p> : <Bar
                data={chartData}
                options={{
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        title: {
                            display: true,
                            text: 'Distribución por activo (último día)',
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1,
                            ticks: {
                                callback: function(value) {
                                    return (value * 100).toFixed(0) + '%';
                                },
                            },
                            title: {
                                display: true,
                                text: 'Peso (%)'
                            }
                        },
                        x: {
                            ticks: {
                                maxRotation: 90,
                                minRotation: 45,
                            }
                        }
                    },
                }}
            />
            }
        </div>
    );
};

export default PortfolioChart;
