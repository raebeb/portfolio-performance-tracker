import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const PortfolioChart = () => {
    const [data, setData] = useState([]);
    const [startDate, setStartDate] = useState(new Date('2022-03-08'));
    const [endDate, setEndDate] = useState(new Date('2022-03-20'));
    const [chartData, setChartData] = useState(null);

    const [portfolioId, setPortfolioId] = useState(1);

    useEffect(() => {
        const fetchData = async () => {
            const fechaInicio = startDate.toISOString().split('T')[0];
            const fechaFin = endDate.toISOString().split('T')[0];

            try {
                const response = await fetch(
                    `http://localhost:8000/api/portfolios/${portfolioId}/summary/?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`
                );
                const json = await response.json();
                setData(json);
            } catch (error) {
                console.error('Error al obtener los datos:', error);
            }
        };

        fetchData();
    }, [startDate, endDate, portfolioId]);

    useEffect(() => {
        if (!data || data.length === 0) return;

        const labels = data.map(item => item.date);
        const allCategories = Object.keys(data[0].weights);

        const datasets = allCategories.map((category, i) => ({
            label: category,
            data: data.map(day => day.weights[category]),
            borderColor: `hsl(${i * 25}, 70%, 50%)`,
            backgroundColor: `hsla(${i * 25}, 70%, 50%, 0.3)`,
            fill: false,
            tension: 0.3
        }));

        setChartData({
            labels,
            datasets
        });
    }, [data]);

    return (
        <div style={{ width: '100%', padding: '2rem' }}>
            <h2 style={{ textAlign: 'center' }}>Distribución de Pesos por Activo</h2>

            <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center', marginBottom: '2rem' }}>
                <div>
                    <label>Fecha inicio</label><br />
                    <DatePicker selected={startDate} onChange={setStartDate} />
                </div>
                <div>
                    <label>Fecha fin</label><br />
                    <DatePicker selected={endDate} onChange={setEndDate} />
                </div>
                <div>
                    <label>ID del Portafolio</label><br />
                    <input
                        type="number"
                        value={portfolioId}
                        onChange={(e) => setPortfolioId(parseInt(e.target.value))}
                        style={{ padding: '0.5rem', borderRadius: '5px', border: '1px solid #ccc', width: '100px' }}
                    />
                </div>
            </div>

            <div style={{ width: '100%', height: '600px' }}>
                {chartData ? (
                    <Line
                        data={chartData}
                        options={{
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'right', // <-- esto mejora muchísimo
                                    labels: {
                                        boxWidth: 20,
                                        padding: 10
                                    }
                                },
                                title: {
                                    display: false
                                }
                            },
                            layout: {
                                padding: 10
                            },
                            responsive: true
                        }}
                    />
                ) : (
                    <p>Cargando datos...</p>
                )}
            </div>
        </div>
    );
};

export default PortfolioChart;
