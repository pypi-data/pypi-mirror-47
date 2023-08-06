# mlcollect

#HDF5 Data
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
labels = le.fit_transform(labels)

dataset = HDF5DatasetWriter((len(imagePaths), 512 * 7 * 7), args["output"], dataKey="features", bufSize=args["buffer_size"])
dataset.storeClassLabels(le.classes_)

batchImages = np.vstack(batchImages)
features = model.predict(batchImages, batch_size=bs)
features = features.reshape((features.shape[0], 512 * 7 * 7))
dataset.add(features, batchLabels)

# initialize the training and validation dataset generators
trainGen = HDF5DatasetGenerator(config.TRAIN_HDF5, 128, aug=aug, preprocessors=[pp, mp, iap], classes=2)
valGen = HDF5DatasetGenerator(config.VAL_HDF5, 128, preprocessors=[sp, mp, iap], classes=2)

# train the network
model.fit_generator(
    trainGen.generator(),
    steps_per_epoch=trainGen.numImages // 128,
    validation_data=valGen.generator(),
    validation_steps=valGen.numImages // 128,
    epochs=75,
    max_queue_size=128 * 2,
    callbacks=callbacks, verbose=1)