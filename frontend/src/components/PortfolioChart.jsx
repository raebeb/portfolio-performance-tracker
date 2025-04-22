import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend, Filler);

const PortfolioChart = () => {
    const [data, setData] = useState([]);
    const [startDate, setStartDate] = useState(new Date('2022-03-08'));
    const [endDate, setEndDate] = useState(new Date('2022-03-20'));
    const [portfolioId, setPortfolioId] = useState(1);

    const [weightsChart, setWeightsChart] = useState(null);
    const [valueChart, setValueChart] = useState(null);

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

        // --- Pesos (w_{i,t}) ---
        const allCategories = Object.keys(data[0].weights);

        const datasetsWeights = allCategories.map((category, i) => ({
            label: category,
            data: data.map(day => day.weights[category]),
            backgroundColor: `hsla(${i * 30}, 70%, 60%, 0.5)`,
            borderColor: `hsl(${i * 30}, 70%, 40%)`,
            fill: true,
            tension: 0.3,
            stack: 'stack1'
        }));

        setWeightsChart({
            labels,
            datasets: datasetsWeights
        });

        // --- Valor total (V_t) ---
        setValueChart({
            labels,
            datasets: [
                {
                    label: 'Valor total del portafolio',
                    data: data.map(day => day.total_value),
                    borderColor: '#1f77b4',
                    backgroundColor: 'rgba(31, 119, 180, 0.2)',
                    fill: false,
                    tension: 0.3
                }
            ]
        });
    }, [data]);

    return (
        <div style={{ width: '100%', padding: '2rem' }}>
            <h2 style={{ textAlign: 'center' }}>Evolución del Portafolio</h2>

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

            {/* Gráfico de pesos */}
            <div style={{ width: '100%', height: '400px', marginBottom: '3rem' }}>
                {weightsChart ? (
                    <Line
                        data={weightsChart}
                        options={{
                            maintainAspectRatio: false,
                            stacked: true,
                            plugins: {
                                legend: { position: 'bottom' }
                            },
                            responsive: true
                        }}
                    />
                ) : (
                    <p>Cargando gráfico de pesos...</p>
                )}
            </div>

            {/* Gráfico de valor total */}
            <div style={{ width: '100%', height: '400px' }}>
                {valueChart ? (
                    <Line
                        data={valueChart}
                        options={{
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { position: 'bottom' }
                            },
                            responsive: true
                        }}
                    />
                ) : (
                    <p>Cargando gráfico de valor...</p>
                )}
            </div>
        </div>
    );
};

export default PortfolioChart;
