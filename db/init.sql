CREATE TABLE IF NOT EXISTS hotel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    adresse TEXT NOT NULL,
    UNIQUE KEY uq_hotel_nom (nom)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    tel VARCHAR(20) NOT NULL,
    UNIQUE KEY uq_client_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS chambre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    type ENUM('simple', 'double', 'suite') NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    etat ENUM('libre', 'occupee', 'maintenance') NOT NULL DEFAULT 'libre',
    hotel_id INT NOT NULL,
    CONSTRAINT fk_chambre_hotel FOREIGN KEY (hotel_id) REFERENCES hotel(id) ON DELETE CASCADE,
    UNIQUE KEY uq_chambre_hotel_numero (hotel_id, numero)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    chambre_id INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    status ENUM('confirmee', 'annulee') NOT NULL DEFAULT 'confirmee',
    CONSTRAINT fk_reservation_client FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE,
    CONSTRAINT fk_reservation_chambre FOREIGN KEY (chambre_id) REFERENCES chambre(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Données de démonstration
INSERT INTO hotel (nom, adresse) VALUES
    ('Paris', '25 avenue des Champs-Élysées, 75008 Paris'),
    ('Lyon', '12 rue de la République, 69001 Lyon')
ON DUPLICATE KEY UPDATE adresse = VALUES(adresse);

INSERT INTO client (nom, email, tel) VALUES
    ('Alice Martin', 'alice.martin@example.com', '+33102030405'),
    ('Bruno Lefevre', 'bruno.lefevre@example.com', '+33455667788')
ON DUPLICATE KEY UPDATE nom = VALUES(nom), tel = VALUES(tel);

INSERT INTO chambre (numero, type, prix, etat, hotel_id)
VALUES ('101', 'double', 129.00, 'libre', 1)
ON DUPLICATE KEY UPDATE prix = VALUES(prix), etat = VALUES(etat);

INSERT INTO chambre (numero, type, prix, etat, hotel_id)
VALUES ('102', 'suite', 189.00, 'libre', 1)
ON DUPLICATE KEY UPDATE prix = VALUES(prix), etat = VALUES(etat);

INSERT INTO chambre (numero, type, prix, etat, hotel_id)
VALUES ('201', 'double', 109.00, 'libre', 2)
ON DUPLICATE KEY UPDATE prix = VALUES(prix), etat = VALUES(etat);
