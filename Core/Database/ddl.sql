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

ALTER TABLE VersoesHardware (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mlfb VARCHAR(50) NOT NULL,
    versao VARCHAR(50) NOT NULL,
    FOREIGN KEY (mlfb) REFERENCES IHM_List(mlfb),
    FOREIGN KEY (mlfb) REFERENCES IO_List(mlfb),
    FOREIGN KEY (mlfb) REFERENCES CPU_List(mlfb),
    UNIQUE(mlfb, versao)
);


SELECT * FROM VersoesHardware WHERE mlfb = '6ES7 132-6BD20-0BA0';

SELECT * FROM IHM_List; WHERE  mlfb = '6ES7 512-1SK01-0AB0'; 214-1AG31-0XB0';

DELETE FROM VersoesHardware WHERE id = 1330;
COMMIT;

UPDATE CPU_List
SET type = 'CONTROLLERS';

SELECT * FROM VersoesHardware WHERE id = 1330;

DELETE FROM IO_List  WHERE mlfb = '6ES7 521-1BH10-0AA0';
WHERE ROWID = (
    SELECT ROWID FROM VersoesHardware
    WHERE mlfb = '6ES7 521-1BH10-0AA0'and versao 'V1.0'

);


Drop TABLE IO_List;
Drop TABLE HMI_List;
DROP TABLE VersoesHardware;



