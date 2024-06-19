CREATE TABLE
    Dll_Path (
        Tia_Version INTEGER PRIMARY KEY,
        path VARCHAR(200)
    );

CREATE TABLE
    CPU_List (
        mlfb VARCHAR(50) PRIMARY KEY,
        type VARCHAR(50),
        description VARCHAR(500)
    );

CREATE TABLE
    IO_List (
        mlfb VARCHAR(50) PRIMARY KEY,
        type VARCHAR(50),
        description VARCHAR(500)
    );

CREATE TABLE VersoesHardware (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mlfb VARCHAR(50) NOT NULL,
    versao VARCHAR(50) NOT NULL,
    FOREIGN KEY (mlfb) REFERENCES IHM_List(mlfb),
    UNIQUE(mlfb, versao)
);


SELECT * FROM IHM_List;
SELECT * FROM VersoesHardware WHERE  mlfb = '6ES7'; 214-1AG31-0XB0';

DELETE FROM VersoesHardware  WHERE mlfb = '6ES7 214-1BE30-0XB0\';and versao = '14.0.0.0';
WHERE ROWID = (
    SELECT ROWID FROM VersoesHardware
    WHERE mlfb = '6AV2 124-0QC02-0AX1'and versao '14.0.0.0'

);


Drop TABLE IHM_List;
Drop TABLE HMI_List;
DROP TABLE VersoesHardware;



