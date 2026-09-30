<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/checker.php';

$action = $_GET['action'] ?? '';

switch ($action) {

    // 1. Get all registered APIs
    case 'get_apis':
        try {
            $stmt = $pdo->query("SELECT * FROM apis ORDER BY id ASC");
            $apis = $stmt->fetchAll();
            echo json_encode(['success' => true, 'data' => $apis]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    // 2. Add a new API
    case 'add_api':
        $raw = file_get_contents('php://input');
        $body = json_decode($raw, true) ?? $_POST;
        
        $name = trim($body['name'] ?? '');
        $url = trim($body['url'] ?? '');
        $method = strtoupper(trim($body['method'] ?? 'GET'));
        $category = trim($body['category'] ?? 'Custom API');
        
        if (empty($name) || empty($url)) {
            echo json_encode(['success' => false, 'error' => 'API Name and URL are required']);
            exit();
        }
        
        try {
            $stmt = $pdo->prepare("INSERT INTO apis (name, url, method, category, last_status) VALUES (?, ?, ?, ?, 'Pending')");
            $stmt->execute([$name, $url, $method, $category]);
            $newId = $pdo->lastInsertId();
            
            // Initial diagnostic ping
            $result = pingEndpoint($url, $method);
            $stmtHist = $pdo->prepare("INSERT INTO api_history (api_id, status_code, response_time, status) VALUES (?, ?, ?, ?)");
            $stmtHist->execute([$newId, $result['status_code'], $result['response_time'], $result['status']]);
            
            $stmtUp = $pdo->prepare("UPDATE apis SET last_status = ? WHERE id = ?");
            $stmtUp->execute([$result['status'], $newId]);
            
            echo json_encode([
                'success' => true,
                'id' => (int)$newId,
                'name' => $name,
                'url' => $url,
                'method' => $method,
                'category' => $category,
                'check' => $result
            ]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    // 3. Delete an API
    case 'delete_api':
        $raw = file_get_contents('php://input');
        $body = json_decode($raw, true) ?? $_POST;
        $id = (int)($body['id'] ?? $_GET['id'] ?? 0);
        
        if ($id <= 0) {
            echo json_encode(['success' => false, 'error' => 'Invalid API ID']);
            exit();
        }
        
        try {
            $stmt = $pdo->prepare("DELETE FROM apis WHERE id = ?");
            $stmt->execute([$id]);
            echo json_encode(['success' => true, 'deleted_id' => $id]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    // 4. Ping a single API
    case 'check_api':
        $id = (int)($_GET['id'] ?? 0);
        if ($id <= 0) {
            echo json_encode(['success' => false, 'error' => 'Invalid API ID']);
            exit();
        }
        
        try {
            $stmt = $pdo->prepare("SELECT * FROM apis WHERE id = ?");
            $stmt->execute([$id]);
            $api = $stmt->fetch();
            
            if (!$api) {
                echo json_encode(['success' => false, 'error' => 'API not found']);
                exit();
            }
            
            $result = pingEndpoint($api['url'], $api['method']);
            
            // Log to history
            $stmtHist = $pdo->prepare("INSERT INTO api_history (api_id, status_code, response_time, status) VALUES (?, ?, ?, ?)");
            $stmtHist->execute([$id, $result['status_code'], $result['response_time'], $result['status']]);
            
            // Update last_status
            $stmtUp = $pdo->prepare("UPDATE apis SET last_status = ? WHERE id = ?");
            $stmtUp->execute([$result['status'], $id]);
            
            echo json_encode([
                'success' => true,
                'api_id' => $id,
                'name' => $api['name'],
                'url' => $api['url'],
                'check' => $result
            ]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    // 5. Ping all registered APIs
    case 'check_all':
        try {
            $stmt = $pdo->query("SELECT * FROM apis");
            $apis = $stmt->fetchAll();
            $results = [];
            
            foreach ($apis as $api) {
                $res = pingEndpoint($api['url'], $api['method']);
                
                $stmtHist = $pdo->prepare("INSERT INTO api_history (api_id, status_code, response_time, status) VALUES (?, ?, ?, ?)");
                $stmtHist->execute([$api['id'], $res['status_code'], $res['response_time'], $res['status']]);
                
                $stmtUp = $pdo->prepare("UPDATE apis SET last_status = ? WHERE id = ?");
                $stmtUp->execute([$res['status'], $api['id']]);
                
                $results[] = [
                    'api_id' => $api['id'],
                    'name' => $api['name'],
                    'check' => $res
                ];
            }
            
            echo json_encode(['success' => true, 'count' => count($results), 'data' => $results]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    // 6. Get Monitoring History
    case 'get_history':
        $apiId = (int)($_GET['api_id'] ?? 0);
        $status = trim($_GET['status'] ?? '');
        $limit = (int)($_GET['limit'] ?? 50);
        
        $sql = "SELECT h.*, a.name AS api_name, a.method, a.url 
                FROM api_history h 
                JOIN apis a ON h.api_id = a.id 
                WHERE 1=1";
        $params = [];
        
        if ($apiId > 0) {
            $sql .= " AND h.api_id = ?";
            $params[] = $apiId;
        }
        if (!empty($status) && $status !== 'all') {
            $sql .= " AND h.status = ?";
            $params[] = $status;
        }
        
        $sql .= " ORDER BY h.checked_at DESC LIMIT " . $limit;
        
        try {
            $stmt = $pdo->prepare($sql);
            $stmt->execute($params);
            $history = $stmt->fetchAll();
            echo json_encode(['success' => true, 'data' => $history]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    // 7. Get Performance Analytics
    case 'get_analytics':
        try {
            $stmtAvg = $pdo->query("SELECT ROUND(AVG(response_time), 1) AS avg_latency FROM api_history WHERE status != 'Failed'");
            $avgLatency = $stmtAvg->fetch()['avg_latency'] ?? 0;
            
            $stmtCounts = $pdo->query("SELECT status, COUNT(*) AS cnt FROM api_history GROUP BY status");
            $statusCounts = $stmtCounts->fetchAll(PDO::FETCH_KEY_PAIR);
            
            $stmtSlow = $pdo->query("SELECT MAX(response_time) AS slowest FROM api_history WHERE status != 'Failed'");
            $slowest = $stmtSlow->fetch()['slowest'] ?? 0;
            
            $stmtComp = $pdo->query("
                SELECT a.name, ROUND(AVG(h.response_time), 1) AS avg_time 
                FROM apis a 
                JOIN api_history h ON a.id = h.api_id 
                WHERE h.status != 'Failed'
                GROUP BY a.id 
                LIMIT 10
            ");
            $comparison = $stmtComp->fetchAll();
            
            echo json_encode([
                'success' => true,
                'avg_latency' => (float)$avgLatency,
                'healthy_count' => (int)($statusCounts['Healthy'] ?? 0),
                'slow_count' => (int)($statusCounts['Slow'] ?? 0),
                'failed_count' => (int)($statusCounts['Failed'] ?? 0),
                'slowest' => (float)$slowest,
                'comparison' => $comparison
            ]);
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
        break;

    default:
        echo json_encode([
            'status' => 'online',
            'service' => 'API Monitoring Backend Engine',
            'version' => '2.0.0',
            'endpoints' => [
                'get_apis', 'add_api', 'delete_api',
                'check_api', 'check_all', 'get_history', 'get_analytics'
            ]
        ]);
        break;
}
?>
