import { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
import fs from "fs";
import path from "path";

const hasAws = Boolean(
  process.env.AWS_ACCESS_KEY_ID &&
  !process.env.AWS_ACCESS_KEY_ID.includes("your-") &&
  process.env.AWS_SECRET_ACCESS_KEY &&
  !process.env.AWS_SECRET_ACCESS_KEY.includes("your-") &&
  process.env.AWS_S3_BUCKET_NAME &&
  !process.env.AWS_S3_BUCKET_NAME.includes("your-")
);

const LOCAL_STORAGE_DIR = path.resolve(process.cwd(), "uploads");
if (!hasAws && !fs.existsSync(LOCAL_STORAGE_DIR)) {
  fs.mkdirSync(LOCAL_STORAGE_DIR, { recursive: true });
}

const s3Config: any = {
  region: process.env.AWS_REGION || "us-east-1",
};

if (hasAws) {
  s3Config.credentials = {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  };
}

const s3Client = new S3Client(s3Config);
const BUCKET_NAME = process.env.AWS_S3_BUCKET_NAME || "";

export async function putFile(key: string, bytes: Buffer): Promise<string> {
  if (!hasAws) {
    const filePath = path.join(LOCAL_STORAGE_DIR, key.replace(/[/\\]/g, "_"));
    await fs.promises.writeFile(filePath, bytes);
    return key;
  }
  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
    Body: bytes,
  });
  await s3Client.send(command);
  return key;
}

export async function getFile(key: string): Promise<Buffer> {
  if (!hasAws) {
    const filePath = path.join(LOCAL_STORAGE_DIR, key.replace(/[/\\]/g, "_"));
    if (fs.existsSync(filePath)) {
      return await fs.promises.readFile(filePath);
    }
    if (fs.existsSync(key)) {
      return await fs.promises.readFile(key);
    }
    throw new Error(`File not found: ${key}`);
  }
  const command = new GetObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
  });
  const response = await s3Client.send(command);
  if (!response.Body) {
    throw new Error("Empty body returned from S3");
  }
  const byteArray = await response.Body.transformToByteArray();
  return Buffer.from(byteArray);
}

export async function deleteFile(key: string): Promise<void> {
  if (!hasAws) {
    const filePath = path.join(LOCAL_STORAGE_DIR, key.replace(/[/\\]/g, "_"));
    if (fs.existsSync(filePath)) {
      await fs.promises.unlink(filePath).catch(() => {});
    }
    return;
  }
  const command = new DeleteObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
  });
  try {
    await s3Client.send(command);
  } catch (err) {
    console.error("Error deleting file from S3:", err);
  }
}
