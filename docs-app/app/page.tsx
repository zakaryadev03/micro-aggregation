export default function DocPage() {
  return (
    <main className="bg-white text-gray-900 p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">About the Platform</h1>

        <section className="mb-10">
          <p className="text-gray-700 leading-relaxed">
            This platform is a <span className="font-medium">price aggregation system</span> that allows
            users to search for a product by keyword and automatically fetch
            prices from multiple markets.  
            It is built using a <span className="font-medium">microfrontend + microservices architecture</span>,
            ensuring scalability, modularity, and flexibility.
          </p>
        </section>

        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-2">Key Features</h2>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>🔍 Search any product by keyword.</li>
            <li>📊 Fetches prices from different online markets.</li>
            <li>⚡ Aggregates results in real time using RabbitMQ as a message broker.</li>
            <li>🖥️ User-friendly frontend built with Next.js.</li>
            <li>📦 Backend service (Node.js REST API) with database storage for results.</li>
            <li>☁️ Designed with microservices & containerization for easy deployment.</li>
          </ul>
        </section>

        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-2">System Architecture</h2>
          <p className="text-gray-700 mb-4 leading-relaxed">
            Below is the high-level architecture of the system showing how the
            frontend, backend, microservices, broker, and external APIs interact.
          </p>
          <img
            src="\architecture.png"
            alt="System Architecture Diagram"
            className="rounded-lg shadow-lg w-full"
          />
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-2">Technology Stack</h2>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>⚛️ <span className="font-medium">Frontend</span>: Next.js</li>
            <li>🟢 <span className="font-medium">Backend</span>: Node.js (REST API Aggregation Service)</li>
            <li>🐇 <span className="font-medium">Broker</span>: RabbitMQ (AMQP)</li>
            <li>🐘 <span className="font-medium">Database</span>: PostgreSQL (Aggregation DB)</li>
            <li>🐳 <span className="font-medium">Markets</span>: Microservices in Docker containers (python)</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
